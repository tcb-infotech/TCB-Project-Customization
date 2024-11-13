# # Copyright (c) 2024, AjayRaj Mahiwal and contributors
# # For license information, please see license.txt


# import frappe
# from frappe import _

# def execute(filters=None):
#     columns = get_columns()
#     data = get_data(filters)
#     return columns, data

# def get_columns():
#     columns = [
#         {
#             "fieldname": "location",
#             "label": _("Location"),
#             "fieldtype": "Link",
#             "options": "Location",
#             "width": 150
#         }
#     ]
    
#     # Fetch active vehicle types
#     vehicle_types = frappe.get_all(
#         "Vehicle Type",
#         filters={"is_active": 1},
#         fields=["name", "type_name"]
#     )
    
#     # Dynamically add columns for each active vehicle type
#     for type_name in vehicle_types:
#         columns.append({
#             "fieldname": frappe.scrub(type_name.type_name),
#             "label": _(type_name.type_name),
#             "fieldtype": "Int",
#             "width": 100
#         })
    
#     return columns

# def get_data(filters):
#     data = []
    
#     # Get all active vehicle types for column mapping
#     vehicle_types = frappe.get_all(
#         "Vehicle Type",
#         filters={"is_active": 1},
#         fields=["name", "type_name"]
#     )
    
#     # Get all locations
#     locations = frappe.get_all("Location", fields=["name"])
    
#     for location in locations:
#         row = {"location": location.name}
        
#         # For each vehicle type, count vehicles at this location
#         for type_name in vehicle_types:
#             count = frappe.db.count(
#                 "Vehicle",
#                 filters={
#                     "custom_vehicle_location": location.name,
#                     "custom_vehicle_type": type_name.name
#                 }
#             )
#             row[frappe.scrub(type_name.type_name)] = count
            
#         data.append(row)
    
#     return data

# def get_vehicle_details(location):
#     """Function to get vehicle details for drill-down"""
#     return frappe.get_all(
#         "Vehicle",
#         filters={"custom_vehicle_location": location},
#         fields=[
#             "name", 
#             "custom_vehicle_type", 
#             "make",
#             "model",
#             "license_plate",
#             "chassis_no",
#             "vehicle_status"
#         ]
#     )


# import frappe
# from frappe import _

# def execute(filters=None):
#     columns = get_columns()
#     data = get_data(filters)
#     return columns, data

# def get_columns():
#     return [
#         {
#             "fieldname": "name",
#             "label": _("Name"),
#             "fieldtype": "Data",
#             "width": 200
#         },
#         {
#             "fieldname": "vehicle_type",
#             "label": _("Vehicle Type"),
#             "fieldtype": "Link",
#             "options": "Vehicle Type",
#             "width": 150
#         },
#         {
#             "fieldname": "make",
#             "label": _("Make"),
#             "fieldtype": "Data",
#             "width": 120
#         },
#         {
#             "fieldname": "model",
#             "label": _("Model"),
#             "fieldtype": "Data",
#             "width": 120
#         },
#         {
#             "fieldname": "license_plate",
#             "label": _("License Plate"),
#             "fieldtype": "Data",
#             "width": 120
#         },

#     ]

# def get_data(filters):
#     data = []
    
#     # Get all locations
#     locations = frappe.get_all("Location", fields=["name"])
    
#     for location in locations:
#         # Add location row as group
#         location_row = {
#             "name": location.name,
#             "is_group": 1,
#             "indent": 0
#         }
#         data.append(location_row)
        
#         # Get vehicles for this location
#         vehicles = frappe.get_all(
#             "Vehicle",
#             filters={"custom_vehicle_location": location.name},
#             fields=[
#                 "name",
#                 "custom_vehicle_type as vehicle_type",
#                 "make",
#                 "model",
#                 "license_plate",
#                 "custom_vehicle_location",
#             ]
#         )
        
#         # Add vehicle rows with numbering
#         for idx, vehicle in enumerate(vehicles, 1):
#             vehicle_row = {
#                 "name": f"Vehicle - {idx}",
#                 "vehicle_type": vehicle.vehicle_type,
#                 "make": vehicle.make,
#                 "model": vehicle.model,
#                 "license_plate": vehicle.license_plate,
#                 "indent": 1,
#                 "_vehicle_name": vehicle.name  # Store original vehicle name for reference
#             }
#             data.append(vehicle_row)
            
#             # Add the actual vehicle details as a child row
#             detail_row = {
#                 "name": vehicle.name,
#                 "vehicle_type": vehicle.vehicle_type,
#                 "make": vehicle.make,
#                 "model": vehicle.model,
#                 "license_plate": vehicle.license_plate,
#                 "indent": 2
#             }
#             data.append(detail_row)
    
#     return data



import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    columns = [
        {
            "fieldname": "name",
            "label": _("Name"),
            "fieldtype": "Data",
            "width": 200
        }
    ]
    
    # Fetch active vehicle types for the main view
    vehicle_types = frappe.get_all(
        "Vehicle Type",
        filters={"is_active": 1},
        fields=["name", "type_name"]
    )
    
    # Add vehicle type columns for the main view
    for type_name in vehicle_types:
        columns.append({
            "fieldname": frappe.scrub(type_name.type_name),
            "label": _(type_name.type_name),
            "fieldtype": "Int",
            "width": 100
        })
    
    # Add detail columns for the drill-down view
    detail_columns = [
        {
            "fieldname": "vehicle_type",
            "label": _("Vehicle Type"),
            "fieldtype": "Link",
            "options": "Vehicle Type",
            "width": 130
        },
        {
            "fieldname": "model",
            "label": _("Model"),
            "fieldtype": "Data",
            "width": 150
        },
        {
            "fieldname": "license_plate",
            "label": _("License Plate"),
            "fieldtype": "Data",
            "width": 140
        },
        {
            "fieldname": "chassis_no",
            "label": _("Chassis No"),
            "fieldtype": "Data",
            "width": 150
        },
    ]
    
    columns.extend(detail_columns)
    return columns

def get_data(filters):
    data = []
    
    # Get all active vehicle types for column mapping
    vehicle_types = frappe.get_all(
        "Vehicle Type",
        filters={"is_active": 1},
        fields=["name", "type_name"]
    )
    
    # Get all locations
    locations = frappe.get_all("Location", fields=["name"])
    
    for location in locations:
        # Create the main location row with vehicle type counts
        row = {
            "name": location.name,
            "is_group": 1,
            "indent": 0
        }
        
        # Add counts for each vehicle type
        location_total_vehicles = 0
        for type_name in vehicle_types:
            count = frappe.db.count(
                "Vehicle",
                filters={
                    "custom_vehicle_location": location.name,
                    "custom_vehicle_type": type_name.name
                }
            )
            row[frappe.scrub(type_name.type_name)] = count
            location_total_vehicles += count
        

        row["name"] = f"{location.name} - {location_total_vehicles}"
        
        data.append(row)
        
        # Get and add vehicle details for this location
        vehicles = frappe.get_all(
            "Vehicle",
            filters={"custom_vehicle_location": location.name},
            fields=[
                "name",
                "custom_vehicle_type as vehicle_type",
                "model",
                "license_plate",
                "chassis_no",
            ]
        )
        
        # Add individual vehicle rows with indent
        for vehicle in vehicles:
            vehicle_row = {
                "name": vehicle.name,
                "vehicle_type": vehicle.vehicle_type,
                "model": vehicle.model,
                "license_plate": vehicle.license_plate,
                "chassis_no": vehicle.chassis_no,
                "indent": 1
            }
            data.append(vehicle_row)
    
    return data

def get_vehicle_details(location):
    """Helper function to get vehicle details for a specific location"""
    return frappe.get_all(
        "Vehicle",
        filters={"custom_vehicle_location": location},
        fields=[
            "name",
            "custom_vehicle_type",
            "model",
            "license_plate",
            "chassis_no",
        ]
    )