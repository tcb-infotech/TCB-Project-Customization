import frappe

def validate(doc,method):
    if doc.custom_vehicle_type:
        if doc.make!= doc.custom_vehicle_type:
            doc.make= doc.custom_vehicle_type
    

@frappe.whitelist()
def change_vehicle_location(doc):
    v = frappe.get_doc("Vehicle", doc)

    if v.custom_move_to_location:
        frappe.db.set_value("Vehicle", v.name, {
            "custom_vehicle_location": v.custom_move_to_location,
            "custom_move_to_location": ""
        })
        return True 
    return False
