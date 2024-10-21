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
            "width": 150
        },
        {
            "label": _("Site"),
            "fieldname": "site",
            "fieldtype": "Link",
            "options": "Project",
            "width": 120
        },
        {
            "label": _("Supervisor"),
            "fieldname": "supervisor",
            "fieldtype": "Data",
            "width": 200
        },
        {
            "label": _("Watchmen"),
            "fieldname": "watchmen",
            "fieldtype": "Data",
            "width": 200
        },
        {
            "label": _("Labour"),
            "fieldname": "labour",
            "fieldtype": "Data",
            "width": 200
        },
        {
            "label": _("Work"),
            "fieldname": "work",
            "fieldtype": "Small Text",
            "width": 250
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
            "width": 200
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
            AND dt.start_date = %(date)s 
    """
            # dt.docstatus = 1
            # AND dt.end_date >= %(date)s
            # AND dt.project = %(project)s

    if filters.get("project"):
        query += "AND dt.project = %(project)s"
        filters["project"] = filters.project

    timesheets = frappe.db.sql(query, filters, as_dict=True)


    data = []
    for ts in timesheets:
        # Get supervisor details
        supervisors = frappe.db.sql("""
            SELECT user_name 
            FROM `tabProject Supervisor Item`
            WHERE parent = %s
        """, ts.timesheet, as_dict=1)
        
        # Get watchmen details
        watchmen = frappe.db.sql("""
            SELECT user_name 
            FROM `tabProject Watchmen Item`
            WHERE parent = %s
        """, ts.timesheet, as_dict=1)
        
        # Get labour and work details from Gang Leader Item
        labour_details = frappe.db.sql("""
            SELECT 
                user_name,
                work,
                labour_count
            FROM `tabProject Gang Leader Item`
            WHERE parent = %s
        """, ts.timesheet, as_dict=1)
        
        # Format labour details and collect work descriptions
        labour_str = []
        work_descriptions = []
        total_labour = 0
        
        for detail in labour_details:
            if detail.labour_count:
                labour_str.append(f"{detail.user_name}-{detail.labour_count}")
                total_labour += detail.labour_count
            if detail.work:
                work_descriptions.append(detail.work)
        
        row = {
            "id": ts.timesheet,
            "site": ts.site,
            "supervisor": "/".join([s.user_name for s in supervisors]),
            "watchmen": "/".join([w.user_name for w in watchmen]),
            "labour": ", ".join(labour_str),
            "work": "\n".join(work_descriptions),
            "total_staff": (
                len(supervisors) +
                len(watchmen) +
                total_labour
            ),
            "remark": frappe.db.get_value("Direct Timesheet", ts.timesheet, "remarks") or ""
        }
        
        data.append(row)
    
    return data