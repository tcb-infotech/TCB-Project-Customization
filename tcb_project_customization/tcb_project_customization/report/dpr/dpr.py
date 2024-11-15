# Copyright (c) 2024, AjayRaj Mahiwal and contributors
# For license information, please see license.txt


import frappe
from frappe import _

def execute(filters=None):
    if not filters:
        filters = {}
    
    columns = get_columns()
    data = get_report_data(filters)
    
    return columns, data

def get_columns():
    return [
        {
            "label": _("ID"),
            "fieldname": "id",
            "fieldtype": "Link",
            "options": "Direct Timesheet",
            "width": 200
        },
        {
            "label": _("Site (Project)"),
            "fieldname": "site",
            "fieldtype": "Link",
            "options": "Project",
            "width": 200
        },
        {
            "label": _("Supervisor"),
            "fieldname": "supervisor",
            "fieldtype": "Data",
            "width": 300
        },
        {
            "label": _("Watchmen"),
            "fieldname": "watchmen",
            "fieldtype": "Data",
            "width": 300
        },
        {
            "label": _("Labour"),
            "fieldname": "labour",
            "fieldtype": "Data",
            "width": 300
        },
        {
            "label": _("Work"),
            "fieldname": "work",
            "fieldtype": "Small Text",
            "width": 400
        },
        {
            "label": _("Total Staff"),
            "fieldname": "total_staff",
            "fieldtype": "Int",
            "width": 100
        },
        {
            "label": _("Remark"),
            "fieldname": "remark",
            "fieldtype": "Data",
            "width": 500
        }
    ]

def get_report_data(filters):
    # Get timesheets for the specific date
    query = """
        SELECT 
            dt.name as timesheet,
            dt.project,
            dt.project_name as site
        FROM 
            `tabDirect Timesheet` dt
        WHERE 
            dt.company = %(company)s
            AND dt.docstatus = 1
    """

    if filters.get("project"):
        query += "AND dt.project = %(project)s"
        filters["project"] = filters.project

    if filters.get("date"):
        query += "AND dt.start_date = %(date)s"
        filters["start_date"] = filters.date


    timesheets = frappe.db.sql(query, filters, as_dict=True)


    data = []
    for ts in timesheets:
        # Get staff details grouped by designation
        staff_query = """
            SELECT 
                employee_name,
                designation,
                activity_type,
                task,
                labour_count,
                description,
                shift,
                is_gang_leader_present
            FROM 
                `tabDirect Timesheet Staff Item`
            WHERE 
                parent = %s
            ORDER BY 
                designation, employee_name
        """
        
        staff_details = frappe.db.sql(staff_query, ts.timesheet, as_dict=1)
        
        # Initialize dictionaries to store grouped data
        supervisors = []
        watchmen = []
        labour_details = []
        work_descriptions = set()  # Using set to avoid duplicates
        total_labour = 0
        
        # Process staff details based on designation
        for staff in staff_details:
            if staff.designation == "Supervisor":
                supervisors.append(staff.employee_name)
            elif staff.designation == "Watchman":
                watchmen.append(f"{staff.employee_name} ({staff.shift})")
            elif staff.designation == "Gang Leader":
                # Only add to labour details if labour count is greater than 0
                if staff.labour_count and staff.labour_count > 0:
                    labour_details.append(f"{staff.employee_name}-{staff.labour_count}")
                    total_labour += staff.labour_count
                else:
                    labour_details.append(f"{staff.employee_name}")
                
                if(staff.is_gang_leader_present):
                        total_labour += 1   # add one for the gang leader if present
                    
                # Only add work descriptions from Gang Leaders
                if staff.description:
                    work_descriptions.add(staff.description)
        
        row = {
            "id": ts.timesheet,
            "site": ts.site,
            "supervisor": " / ".join(supervisors) if supervisors else "",
            "watchmen": " / ".join(watchmen) if watchmen else "",
            "labour": ", ".join(labour_details) if labour_details else "",  # Will be empty if no labour_details
            "work": " / ".join(work_descriptions) if work_descriptions else "",  # Only Gang Leader work descriptions
            "total_staff": (
                len(supervisors) +
                len(watchmen) +
                total_labour
            ),
            "remark": frappe.db.get_value("Direct Timesheet", ts.timesheet, "remarks") or ""
        }
        
        data.append(row)
    
    return data