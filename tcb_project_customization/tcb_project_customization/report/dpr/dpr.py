import frappe
from frappe import _

def execute(filters=None):
    if not filters:
        filters = {}
    
    columns = get_columns()
    data = get_report_data(filters)
    
    return columns, data


def get_report_data(filters):
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
        project_rows = []

        project_location = frappe.db.get_value("Project", ts.project, "custom_location")

        staff_query = """
            SELECT 
                employee_name,
                designation,
                labour_count,
                description,
                shift,
                activity_type,
                tower_no,
                tower_type,
                team_leader,
                work_start_date,
                work_completion_date
            FROM 
                `tabDirect Timesheet Staff Item`
            WHERE 
                parent = %s
            ORDER BY 
                designation, employee_name
        """
        staff_details = frappe.db.sql(staff_query, ts.timesheet, as_dict=True)

        activity_groups = {}
        for staff in staff_details:
            key = staff.activity_type or "No Activity"
            activity_groups.setdefault(key, []).append(staff)

        for activity_type, group in activity_groups.items():
            work_start_date = group[0].work_start_date if hasattr(group[0], "work_start_date") else ""
            work_completion_date = group[0].work_completion_date if hasattr(group[0], "work_completion_date") else ""
            supervisors = []
            supervisor_works = []
            supervisor_contact = ""
            operators = []
            team_leaders = []
            team_leader_works = []
            watchmen = []
            labour_count = 0
            managers = []
            manager_works = []
            
            completion_label = ""
            if work_start_date and work_completion_date:
                days_taken = (work_completion_date - work_start_date).days
                completion_label = f"{work_completion_date} ({days_taken} days)"
            elif work_completion_date:
                completion_label = str(work_completion_date)

            for staff in group:
                if staff.designation == "Supervisor":
                    supervisors.append(staff.employee_name)
                    if staff.description:
                        supervisor_works.append(f"{staff.employee_name}: {staff.description}")
                    if not supervisor_contact:
                        supervisor_contact = frappe.db.get_value("Employee", {"employee_name": staff.employee_name}, "cell_number") or ""
                elif staff.designation == "Manager":
                    managers.append(staff.employee_name)
                    if staff.description:
                        manager_works.append(f"{staff.employee_name}: {staff.description}")
                elif staff.designation == "Operator":
                    operators.append(staff.employee_name)
                elif staff.team_leader:
                    team_leaders.append(staff.team_leader)
                    if staff.description:
                        team_leader_works.append(f"{staff.team_leader}: {staff.description}")
                    labour_count += staff.labour_count or 0
                elif staff.designation == "Watchman":
                    watchmen.append(f"{staff.employee_name} ({staff.shift})")

            row = {
                "id": ts.timesheet,
                "site": ts.site,
                "work": activity_type,
                "work_start_date": work_start_date,
                "work_completion_date": completion_label,
                "tower_no": group[0].tower_no if hasattr(group[0], "tower_no") else "",
                "tower_type": group[0].tower_type if hasattr(group[0], "tower_type") else "",
                "supervisor_work": ", ".join(supervisors),
                "supervisor_contact": supervisor_contact,
                "supervisor_details": "; ".join(supervisor_works) if supervisor_works else " ",
                "managers": ", ".join(managers),
                "manager_works": "; ".join(manager_works) if manager_works else "",
                "operator_work": ", ".join(operators) if operators else " ",
                "team_leader_work": ", ".join(team_leaders) if team_leaders else " ",
                "team_leader_details": "; ".join(team_leader_works) if team_leader_works else " ",
                "watchmen": ", ".join(watchmen) if watchmen else " ",
                "labour": labour_count,
                "total_staff": len(supervisors) + len(operators) + len(watchmen) + labour_count,
                "remark": frappe.db.get_value("Direct Timesheet", ts.timesheet, "remarks") or ""
            }

            project_rows.append(row)

        vehicle_summary = ""
        if project_location:
            vehicle_data = frappe.db.sql("""
                SELECT custom_vehicle_type, COUNT(*) as count
                FROM `tabVehicle`
                WHERE custom_vehicle_location = %s
                GROUP BY custom_vehicle_type
            """, (project_location,), as_dict=True)

            vehicle_summary = ", ".join(f"{v.custom_vehicle_type}: {v.count}" for v in vehicle_data) if vehicle_data else "No Vehicles"

        if project_rows:
            data.extend(project_rows)
            data.append({
                "site": ts.site,
                "vehicle_summary": vehicle_summary
            })

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
            "label": _("Work Start Date"),
            "fieldname": "work_start_date",
            "fieldtype": "Date",
            "width": 130
        },
        {
            "label": _("Work Completion Date"),
            "fieldname": "work_completion_date",
            "fieldtype": "Data",
            "width": 180
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
            "label": _("Managers"),
            "fieldname": "managers",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": _("Manager Works"),
            "fieldname": "manager_works",
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
            "label": _("Team Leader"),
            "fieldname": "team_leader_work",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": _("Team Leader Work"),
            "fieldname": "team_leader_details",
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
            "width": 300
        },
        {
            "label": _("Vehicle Summary"),
            "fieldname": "vehicle_summary",
            "fieldtype": "Data",
            "width": 300
        }
    ]
