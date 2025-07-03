

import frappe
from frappe import _

def execute(filters=None):
    if not filters:
        filters = {}
    
    columns = get_columns()
    data = get_report_data(filters)
    
    return columns, data


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
        # Fetch staff items for this timesheet
        staff_query = """
            SELECT 
                employee_name,
                designation,
                labour_count,
                description,
                shift,
                activity_type,
                tower_no,
                tower_type
            FROM 
                `tabDirect Timesheet Staff Item`
            WHERE 
                parent = %s
            ORDER BY 
                designation, employee_name
        """
        staff_details = frappe.db.sql(staff_query, ts.timesheet, as_dict=True)

        # Group staff by activity type
        activity_groups = {}
        for staff in staff_details:
            key = staff.activity_type or "No Activity"
            activity_groups.setdefault(key, []).append(staff)

        for activity_type, group in activity_groups.items():
            supervisors = []
            supervisor_works = []
            supervisor_contact = ""
            operators = []
            gang_leaders = []
            gang_leader_works = []
            watchmen = []
            labour_count = 0

            for staff in group:
                if staff.designation == "Supervisor":
                    supervisors.append(staff.employee_name)
                    if staff.description:
                        supervisor_works.append(f"{staff.employee_name}: {staff.description}")
                    # fetch supervisor contact (first one only)
                    if not supervisor_contact:
                        supervisor_contact = frappe.db.get_value("Employee", {"employee_name": staff.employee_name}, "cell_number") or ""
                elif staff.designation == "Operator":
                    operators.append(staff.employee_name)
                elif staff.designation == "Gangleader":
                    gang_leaders.append(staff.employee_name)
                    if staff.description:
                        gang_leader_works.append(f"{staff.employee_name}: {staff.description}")
                    labour_count += staff.labour_count or 0
                elif staff.designation == "Watchman":
                    watchmen.append(f"{staff.employee_name} ({staff.shift})")

            row = {
                "id": ts.timesheet,
                "site": ts.site,
                "work": activity_type,
                "tower_no": group[0].tower_no if hasattr(group[0], "tower_no") else "",
                "tower_type": group[0].tower_type if hasattr(group[0], "tower_type") else "",
                "supervisor_work": ", ".join(supervisors),
                "supervisor_contact": supervisor_contact,
                "supervisor_details": "; ".join(supervisor_works) if supervisor_works else " ",
                "operator_work": ", ".join(operators) if operators else " ",
                "gang_leader_work": ", ".join(gang_leaders) if gang_leaders else " ",
                "gang_leader_details": "; ".join(gang_leader_works) if gang_leader_works else " ",
                "watchmen": ", ".join(watchmen) if watchmen else " ",
                "labour": labour_count,
                "total_staff": len(supervisors) + len(operators) + len(watchmen) + labour_count,
                "remark": frappe.db.get_value("Direct Timesheet", ts.timesheet, "remarks") or ""
            }


            data.append(row)
    
    return data

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
        "label": _("Work"),
        "fieldname": "work",
        "fieldtype": "Link",
        "options": "Activity Type",
        "width": 200
    },
    {
        "label": _("Tower No"),
        "fieldname": "tower_no",
        "fieldtype": "Data",
        "width": 150
    },
    {
        "label": _("Tower Type"),
        "fieldname": "tower_type",
        "fieldtype": "Data",
        "width": 150
    },
    {
        "label": _("Supervisor"),
        "fieldname": "supervisor_work",
        "fieldtype": "Data",
        "width": 150
    },
    {
        "label": _("Supervisor Contact"),
        "fieldname": "supervisor_contact",
        "fieldtype": "Data",
        "width": 130
    },
    {
        "label": _("Supervisor Work"),
        "fieldname": "supervisor_details",
        "fieldtype": "Small Text",
        "width": 250
    },
    {
        "label": _("Operator"),
        "fieldname": "operator_work",
        "fieldtype": "Data",
        "width": 150
    },
    {
        "label": _("Gang Leader"),
        "fieldname": "gang_leader_work",
        "fieldtype": "Data",
        "width": 150
    },
    {
        "label": _("Gang Leader Work"),
        "fieldname": "gang_leader_details",
        "fieldtype": "Small Text",
        "width": 250
    },
    {
        "label": _("Watchmen"),
        "fieldname": "watchmen",
        "fieldtype": "Data",
        "width": 200
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
