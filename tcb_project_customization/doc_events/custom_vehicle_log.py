import frappe
from frappe import utils
import json
from frappe import _

@frappe.whitelist()
def set_vehicle_movement(doc):
    if isinstance(doc, str):
        doc = json.loads(doc)
        
    vehicle_doc = frappe.get_doc('Vehicle', {'license_plate': doc.get('license_plate')})
    
    vehicle_doc.append('custom_vehicle_location_movement_history', {
        'move_from': doc.get('custom_current_location'),
        'move_to': doc.get('custom_move_to'),
        'movement_date': doc.get('date'),
        'last_odometer': doc.get('odometer')
    })
    
    vehicle_doc.save()


@frappe.whitelist()
def set_current_location(license_plate):
    vehicle_doc= frappe.get_doc('Vehicle',{'license_plate':license_plate})

    last_value=None
    last_odo= None

    if(vehicle_doc.custom_vehicle_location_movement_history and len(vehicle_doc.custom_vehicle_location_movement_history)>0):
        last_row= vehicle_doc.custom_vehicle_location_movement_history[-1]
        last_value= last_row.move_to
        last_odo= last_row.last_odometer

    return {
        'location':last_value,
        'odometer':last_odo
    }



@frappe.whitelist()
def get_draft_entries(doc):
    if isinstance(doc, str):
        doc = json.loads(doc)

    draft_entries = frappe.db.get_list('Vehicle Log',
        filters=[
            ['docstatus','=', 0],
            ['license_plate','=', doc.get('license_plate')],
            ['name','!=',doc.get('name')]
        ],
        fields=['name'],
        order_by='creation desc'
    )
    
    return draft_entries


# AJAY's Code
# def get_draft_entries(self, *args, **kwargs):
#     # if isinstance(doc, str):
#     #     doc = json.loads(doc)

#     doc= frappe.get_doc('Vehicle Log',self.name)

#     draft_entries = frappe.db.get_list('Vehicle Log',
#         filters=[
#             ['docstatus','=', 0],
#             ['license_plate','=', doc.license_plate],
#             ['name','!=',doc.name]
#         ],
#         fields=['name'],
#         order_by='creation desc'
#     )
#     if(draft_entries and len(draft_entries)>0):
#         frappe.throw('You cannot submit')
    


# @frappe.whitelist()
# def greet():
#     return frappe.db.sql("""
#     select license_plate, custom_vehicle_location, model from `tabVehicle`;
# """,as_dict=True)