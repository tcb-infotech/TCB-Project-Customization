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
            "label": _("Supervisor and Work"),
            "fieldname": "supervisor_work",
            "fieldtype": "Small Text",
            "width": 300
        },
        {
            "label": _("Operator and Work"),
            "fieldname": "operator_work",
            "fieldtype": "Small Text",
            "width": 300
        },
        {
            "label": _("Gang Leader and Work"),
            "fieldname": "gang_leader_work",
            "fieldtype": "Small Text",
            "width": 300
        },
        {
            "label": _("Watchmen"),
            "fieldname": "watchmen",
            "fieldtype": "Data",
            "width": 300
        },
        {
            "label": _("Labour Count"),
            "fieldname": "labour",
            "fieldtype": "Int",
            "width": 100
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
    # Fetch timesheets based on filters
    query = """
        SELECT 
            dt.name AS timesheet,
            dt.project,
            dt.project_name AS site
        FROM 
            `tabDirect Timesheet` dt
        WHERE 
            dt.company = %(company)s
            AND dt.docstatus = 1
    """

    if filters.get("project"):
        query += " AND dt.project = %(project)s"

    if filters.get("date"):
        query += " AND dt.start_date = %(date)s"

    timesheets = frappe.db.sql(query, filters, as_dict=True)

    data = []
    for ts in timesheets:
        # Fetch staff details for each timesheet
        staff_query = """
            SELECT 
                employee_name,
                designation,
                labour_count,
                description,
                shift
            FROM 
                `tabDirect Timesheet Staff Item`
            WHERE 
                parent = %s
            ORDER BY 
                designation, employee_name
        """
        staff_details = frappe.db.sql(staff_query, ts.timesheet, as_dict=1)

        # Group and process staff data
        supervisors_work = []
        operators_work = []
        gang_leaders_work = []
        watchmen = []
        labour_count = 0

        for staff in staff_details:
            work = f"{staff.employee_name}: {staff.description}" if staff.description else staff.employee_name
            if staff.designation == "Supervisor":
                supervisors_work.append(work)
            elif staff.designation == "Operator":
                operators_work.append(work)
            elif staff.designation == "Gangleader":
                gang_leaders_work.append(work)
                labour_count += staff.labour_count or 0
            elif staff.designation == "Watchman":
                watchmen.append(f"{staff.employee_name} ({staff.shift})")

        # Prepare row data
        row = {
            "id": ts.timesheet,
            "site": ts.site,
            "supervisor_work": " / ".join(supervisors_work),
            "operator_work": " / ".join(operators_work),
            "gang_leader_work": " / ".join(gang_leaders_work),
            "watchmen": " / ".join(watchmen),
            "labour": labour_count,
            "total_staff": len(supervisors_work) + len(operators_work) + len(watchmen) + labour_count,
            "remark": frappe.db.get_value("Direct Timesheet", ts.timesheet, "remarks") or ""
        }
        data.append(row)
    
    return data
