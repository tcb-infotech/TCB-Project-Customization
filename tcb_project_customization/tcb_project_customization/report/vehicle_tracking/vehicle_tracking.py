# Copyright (c) 2024, AjayRaj Mahiwal and contributors
# For license information, please see license.txt


import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns(filters)
    data = get_data(filters)
    return columns, data

def get_columns(filters):
    return [
        {
            "label": _("Vehicle/History"),
            "fieldname": "name",
            "fieldtype": "Link",
            "options": "Vehicle",
            "width": 200
        },
        {
            "label": _("Current Location"),
            "fieldname": "custom_project_name",
            "fieldtype": "Data",
            "width": 200
        },
        {
            "label": _("Project"),
            "fieldname": "custom_project",
            "fieldtype": "Link",
            "options": "Project",
            "width": 150
        },
        {
            "label": _("Make"),
            "fieldname": "make",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": _("Model"),
            "fieldname": "model",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": _("Last Odometer"),
            "fieldname": "last_odometer",
            "fieldtype": "Float",
            "width": 150
        },
        {
            "label": _("Move From"),
            "fieldname": "move_from",
            "fieldtype": "Link",
            "options": "Project",
            "width": 150
        },
        {
            "label": _("Move To"),
            "fieldname": "move_to",
            "fieldtype": "Link",
            "options": "Project",
            "width": 150
        },
        {
            "label": _("Movement Date"),
            "fieldname": "movement_date",
            "fieldtype": "Datetime",
            "width": 180
        }
    ]

def get_data(filters):
    data = []
    vehicles = get_vehicle_data(filters)
    
    for vehicle in vehicles:
        # Add parent row (vehicle)
        vehicle.update({
            "indent": 0,
            "is_group": 1,  # This makes it expandable
            "vehicle_id": vehicle.name  # Store vehicle ID for child rows
        })
        data.append(vehicle)
        
        # Get and add movement history as child rows
        movement_history = get_movement_history(vehicle.name)
        index = 0
        for history in movement_history:
            index += 1
            history.update({
                "indent": 1,
                # "name":  history.movement_id,  # Unique identifier for the history row
                "name":  f"Movement-{index}",  # Unique identifier for the history row
                "custom_project_name": "",  # Clear parent fields in child rows
                "make": "",
                "model": "",
                "parent_vehicle": vehicle.name
            })
            data.append(history)
    
    return data

def get_vehicle_data(filters):
    conditions = get_conditions(filters)
    
    query = """
        SELECT 
            v.name,
            v.custom_project_name,
            v.custom_project,
            v.make,
            v.model,
            COALESCE(
                (SELECT last_odometer 
                 FROM `tabVehicle Location History Item` vh 
                 WHERE vh.parent = v.name 
                 ORDER BY vh.movement_date DESC 
                 LIMIT 1),
                v.last_odometer
            ) as last_odometer
        FROM
            `tabVehicle` v
        WHERE
            1=1
            {conditions}
        ORDER BY
            v.name
    """.format(conditions=conditions)
    
    return frappe.db.sql(query, filters, as_dict=1)

def get_movement_history(vehicle):
    query = """
        SELECT 
            name as movement_id,
            parent,
            move_from,
            move_to,
            movement_date,
            last_odometer
        FROM
            `tabVehicle Location History Item`
        WHERE
            parent = %s
        ORDER BY
            movement_date ASC
    """
    
    return frappe.db.sql(query, vehicle, as_dict=1)

def get_conditions(filters):
    conditions = []
    
    if filters.get("vehicle"):
        conditions.append("AND v.name = %(vehicle)s")
        
    if filters.get("custom_project"):
        conditions.append("AND v.custom_project = %(custom_project)s")
        
    if filters.get("make"):
        conditions.append("AND v.make = %(make)s")
        
    if filters.get("model"):
        conditions.append("AND v.model = %(model)s")
        
    return " ".join(conditions)