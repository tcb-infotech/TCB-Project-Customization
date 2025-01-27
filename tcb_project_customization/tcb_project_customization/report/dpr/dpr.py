

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

        # Separate staff details 
        supervisors = []
        supervisor_works = []
        operators = []
        # operator_works = []
        gang_leaders = []
        gang_leader_works = []
        watchmen = []
        labour_count = 0

        for staff in staff_details:
            if staff.designation == "Supervisor":
                supervisors.append(staff.employee_name)
                if staff.description:
                    supervisor_works.append(f"{staff.employee_name}: {staff.description}")
            elif staff.designation == "Operator":
                operators.append(staff.employee_name)
                # if staff.description:
                #     operator_works.append(f"{staff.employee_name}: {staff.description}")
            elif staff.designation == "Gangleader":
                gang_leaders.append(staff.employee_name)
                if staff.description:
                    gang_leader_works.append(f"{staff.employee_name}: {staff.description}")
                labour_count += staff.labour_count or 0
            elif staff.designation == "Watchman":
                watchmen.append(f"{staff.employee_name} ({staff.shift})")

        # Prepare row data with full lists
        row = {
            "id": ts.timesheet,
            "site": ts.site,
            "supervisor_work": ", ".join(supervisors),
            "supervisor_details": "; ".join(supervisor_works) if supervisor_works else " ",
            "operator_work": ", ".join(operators) if operators else " ",
            # "operator_details": "; ".join(operator_works) if operator_works else " ",
            "gang_leader_work": ", ".join(gang_leaders) if gang_leaders else " ",
            "gang_leader_details": "; ".join(gang_leader_works) if gang_leader_works else " ",
            "watchmen": ", ".join(watchmen) if watchmen else " ",
            "labour": labour_count,
            "total_staff": len(supervisors) + len(operators) + len(watchmen) + labour_count,
            "remark": frappe.db.get_value("Direct Timesheet", ts.timesheet, "remarks") or ""
        }
        blankrow = {
            "id": "",
            "site": "",
            "supervisor_work": "",
            "supervisor_details": "",
            "operator_work": "",
            # "operator_details": "; ".join(operator_works) if operator_works else " ",
            "gang_leader_work": "",
            "gang_leader_details": "",
            "watchmen": "",
            "labour": "",
            "total_staff": "",
            "remark": ""
        }
        data.append(row)
        data.append(blankrow)
    
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
            "label": _("Supervisor"),
            "fieldname": "supervisor_work",
            "fieldtype": "Data",
            "width": 150
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
        # {
        #     "label": _("Operator Work"),
        #     "fieldname": "operator_details",
        #     "fieldtype": "Small Text",
        #     "width": 250
        # },
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
