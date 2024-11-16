import frappe

def validate(doc,method):
    if doc.custom_vehicle_type:
        if doc.make!= doc.custom_vehicle_type:
            doc.make= doc.custom_vehicle_type