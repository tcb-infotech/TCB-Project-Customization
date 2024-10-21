# Copyright (c) 2024, AjayRaj Mahiwal and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, time_diff_in_hours, today
from frappe import _
from collections import defaultdict

class DirectTimesheet(Document):
    def validate(self):
        self.validate_dates()
        self.set_dates()
        self.calculate_hours()
        
    def on_submit(self):
        try:
            grouped_by_gang_leader = defaultdict(list)
            for row in self.time_logs:
                leader = row.gang_leader
                grouped_by_gang_leader[leader].append(row)
            
            grouped_by_gang_leader = dict(grouped_by_gang_leader)
            
            for leader, group in grouped_by_gang_leader.items():
                # print("leader", leader)
                # print(group)
                
                ts = frappe.new_doc("Timesheet")
                
                if self.amended_from and len(group):
                    ts.amended_from = group[0].timesheet_id
                    
                ts.company = self.company
                ts.employee = leader
                ts.customer = self.customer

                if hasattr(ts, 'custom_direct_timesheet'):
                    ts.custom_direct_timesheet = self.name

                
                for row in group:
                    ts.append("time_logs", {
                        "activity_type": row.activity_type,
                        "task": row.task,
                        "project": self.project,
                        "from_time": row.from_time,
                        "to_time": row.to_time,
                        "hours": row.hours,
                        "description": row.description
                    })
                
                ts.save()
                ts.submit()
                
                # Update timesheet_id in the original time_logs
                for row in group:
                    # Update at database level
                    frappe.db.set_value('Direct Timesheet Item', row.name, 'timesheet_id', ts.name)
                    # Update in current document
                    row.timesheet_id = ts.name
                
                # Commit the database changes
                frappe.db.commit()
                
        except Exception as e:
            frappe.throw(f"Can't Create TimeSheet Due To Internal Error: {str(e)}")

    
    
    # def on_cancel(self):
    #     try:
    #         timesheet_set = set()
            
    #         # Debug print to see what's in time_logs
    #         # print("time_logs content:", self.time_logs)
            
    #         for time_log in self.time_logs:
    #             # print("Processing time_log:", {
    #             #     "name": time_log.name,
    #             #     "gang_leader": time_log.gang_leader,
    #             #     "timesheet_id": time_log.timesheet_id
    #             # })
                
    #             if time_log.timesheet_id:
    #                 timesheet_set.add(time_log.timesheet_id)
            
    #         # print("Final timesheet_set:", timesheet_set)
            
    #         if not timesheet_set:
    #             frappe.throw("No timesheets found to cancel. Please check if timesheet_ids are properly saved.")
            
    #         for ts in timesheet_set:
    #             # print("Processing Timesheet:", ts)
    #             ts_doc = frappe.get_doc("Timesheet", ts)
                
    #             if ts_doc.docstatus != 2:
    #                 ts_doc.cancel()
    #             else:
    #                 frappe.throw(f"Timesheet {ts} is already canceled.")
        
    #     except Exception as e:
    #         frappe.throw(f"Can't Cancel Due To Internal Error: {str(e)}")
            

            
    def calculate_hours(self):
        for row in self.time_logs:
            if row.to_time and row.from_time:
                row.hours = time_diff_in_hours(row.to_time, row.from_time)
        

    def validate_dates(self):
        for data in self.time_logs:
            if data.from_time and data.to_time and time_diff_in_hours(data.to_time, data.from_time) < 0:
                frappe.throw(_("To date cannot be before from date"))
            
    def set_dates(self):
        if self.docstatus < 2 and self.time_logs:
            # start_date = min(getdate(d.from_time) for d in self.time_logs)
            start_date = today()
            end_date = max(getdate(d.to_time) for d in self.time_logs)

            if start_date and end_date:
                self.start_date = getdate(start_date)
                self.end_date = getdate(end_date)


@frappe.whitelist()
def sync_project_details_with_timesheet(timesheet_id, project):
    """
    Syncs project details with timesheet using minimal required data
    
    Args:
        timesheet_id: ID of the Direct Timesheet document
        project: Project ID to sync from
    Returns:
        dict: Status and message
    """
    try:
        # Validate inputs
        if not timesheet_id:
            frappe.throw(_("Timesheet ID is required"))
        if not project:
            frappe.throw(_("Project is required"))

        # Get the documents
        timesheet_doc = frappe.get_doc("Direct Timesheet", timesheet_id)
        project_doc = frappe.get_doc("Project", project)

        timesheet_doc.project = project
        
        # Clear existing entries
        timesheet_doc.supervisor_details = []
        timesheet_doc.gang_leader_details = []
        timesheet_doc.watchmen_details = []
        
        # Sync supervisor details with correct fields
        for supervisor in project_doc.custom_supervisor_details:
            timesheet_doc.append("supervisor_details", {
                "supervisor_id": supervisor.supervisor_id,
                "user_name": supervisor.user_name,
                "work": supervisor.work
            })
        
        # Sync gang leader details with correct fields
        for gang_leader in project_doc.custom_gang_leader_details:
            timesheet_doc.append("gang_leader_details", {
                "gang_leader_id": gang_leader.gang_leader_id,
                "user_name": gang_leader.user_name,
                "labour_count": gang_leader.labour_count,
                "work": gang_leader.work
            })
        
        # Sync watchmen details with correct fields
        for watchman in project_doc.custom_watchmen_details:
            timesheet_doc.append("watchmen_details", {
                "watchman_id": watchman.watchman_id,
                "user_name": watchman.user_name,
                "shift": watchman.shift
            })
        
        # Save the document
        timesheet_doc.flags.ignore_validate = True
        timesheet_doc.flags.ignore_mandatory = True
        timesheet_doc.save()
        frappe.db.commit()
        
        return {
            "status": "success",
            "message": _("Project details synced successfully")
        }
        
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Project Sync Error"))
        frappe.throw(_("Error syncing project details: {0}").format(str(e)))
