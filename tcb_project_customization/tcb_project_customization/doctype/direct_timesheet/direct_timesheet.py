# Copyright (c) 2024, AjayRaj Mahiwal and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, time_diff_in_hours, today, add_days
from frappe import _
from collections import defaultdict

class DirectTimesheet(Document):
    def validate(self):
    # Unique SuperVisors
        employee_set = set()
        unique_details = []

        for emp in self.staff_details:
            if emp.employee not in employee_set:
                unique_details.append(emp)
                employee_set.add(emp.employee)

        self.staff_details = []
        for emp in unique_details:
            self.append("staff_details",emp)
        #     self.validate_dates()
        #     self.set_dates()
    #     self.calculate_hours()
        
    # New
    # def on_submit(self):
    #     try:
    #         grouped_by_employee = defaultdict(list)
    #         for row in self.staff_details:
    #             leader = row.employee
    #             grouped_by_employee[leader].append(row)
            
    #         grouped_by_employee = dict(grouped_by_employee)
            
    #         for leader, group in grouped_by_employee.items():
    #             # print("leader", leader)
    #             # print(group)
                
    #             ts = frappe.new_doc("Timesheet")
                
    #             if self.amended_from and len(group):
    #                 ts.amended_from = group[0].timesheet_id
                    
    #             ts.company = self.company
    #             ts.employee = leader
    #             ts.customer = self.customer

    #             if hasattr(ts, 'custom_direct_timesheet'):
    #                 ts.custom_direct_timesheet = self.name

                
    #             for row in group:
    #                 ts.append("time_logs", {
    #                     "activity_type": row.activity_type,
    #                     "task": row.task,
    #                     "project": self.project,
    #                     "from_time": today(),
    #                     "to_time": add_days(today(),1),
    #                     "hours": 24,
    #                     "description": row.description
    #                 })
                
    #             ts.save()
    #             ts.submit()
                
    #             # Update timesheet_id in the original staff_details
    #             for row in group:
    #                 # Update at database level
    #                 frappe.db.set_value('Direct Timesheet Staff Item', row.name, 'timesheet_id', ts.name)
    #                 # Update in current document
    #                 row.timesheet_id = ts.name
                
    #             # Commit the database changes
    #             frappe.db.commit()
                
    #     except Exception as e:
    #         frappe.throw(f"Can't Create TimeSheet Due To Internal Error: {str(e)}")

    
    # OLD
    # def on_cancel(self):
    #     try:
    #         timesheet_set = set()
            
    #         # Debug print to see what's in staff_details
    #         # print("staff_details content:", self.staff_details)
            
    #         for time_log in self.staff_details:
    #             # print("Processing time_log:", {
    #             #     "name": time_log.name,
    #             #     "employee": time_log.employee,
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
            

            
    # def calculate_hours(self):
    #     for row in self.staff_details:
    #         if row.to_time and row.from_time:
    #             row.hours = time_diff_in_hours(row.to_time, row.from_time)
        

    # def validate_dates(self):
    #     for data in self.staff_details:
    #         if data.from_time and data.to_time and time_diff_in_hours(data.to_time, data.from_time) < 0:
    #             frappe.throw(_("To date cannot be before from date"))
            
    # def set_dates(self):
    #     if self.docstatus < 2 and self.staff_details:
    #         # start_date = min(getdate(d.from_time) for d in self.staff_details)
    #         start_date = today()
    #         end_date = max(getdate(d.to_time) for d in self.staff_details)

    #         if start_date and end_date:
    #             self.start_date = getdate(start_date)
    #             self.end_date = getdate(end_date)


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
        direct_timesheet_doc = frappe.get_doc("Direct Timesheet", timesheet_id)
        project_doc = frappe.get_doc("Project", project)

        direct_timesheet_doc.project = project
        
        # Clear existing entries
        direct_timesheet_doc.staff_details = []
        

        # Sync gang leader details with correct fields
        for employee in project_doc.custom_staff_details:
            direct_timesheet_doc.append("staff_details", {
                "employee": employee.employee,
                "activity_type": employee.activity_type,
                "task": employee.task,
                "labour_count": employee.labour_count or 0,
                "description":employee.description,
            })

        
        # Save the document
        direct_timesheet_doc.flags.ignore_validate = True
        direct_timesheet_doc.flags.ignore_mandatory = True
        direct_timesheet_doc.save()
        frappe.db.commit()
        
        return {
            "status": "success",
            "message": _("Project details synced successfully")
        }
        
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Project Sync Error"))
        frappe.throw(_("Error syncing project details: {0}").format(str(e)))






# REMOVE SUBMITTED ENTRIES
# def del_dpr():
#     start = "2025-08-13 00:00:00"
#     end = "2025-08-13 23:59:59"

#     dpr_list = frappe.db.get_all(
#         "Direct Timesheet",
#         filters={"creation": ["between", [start, end]],"docstatus":2},
#         pluck="name"
#     )

#     for entry in dpr_list:
#         # doc = frappe.get_doc("Direct Timesheet",entry)
#         # doc.cancel()
#         frappe.delete_doc("Direct Timesheet",entry)