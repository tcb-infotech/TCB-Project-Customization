import frappe
from frappe import utils
import json
from frappe import _

@frappe.whitelist()
def set_vehicle_movement(doc):
    if isinstance(doc, str):
        doc = json.loads(doc)
    
    vehicle_doc = frappe.get_doc('Vehicle', {'license_plate': doc.get('license_plate')})
    
    vehicle_doc.custom_vehicle_location = doc.get('custom_move_to')

    if vehicle_doc:
        vehicle_doc.append('custom_vehicle_location_movement_history', {
            'move_from': doc.get('custom_current_location'),
            'move_to': doc.get('custom_move_to'),
            'movement_date': doc.get('date'),
            'last_odometer': doc.get('odometer'),
            'custom_vehicle_log':doc.get('name')
        })
        
        vehicle_doc.save()
        # frappe.db.commit()
    else:
        frappe.throw(_("Vehicle with license plate {0} not found.").format(doc.get('license_plate')))


@frappe.whitelist()
def set_current_location(license_plate):
    vehicle_doc= frappe.get_doc('Vehicle',{'license_plate':license_plate})

    last_value=None 
    last_odo= None

    if(vehicle_doc.custom_vehicle_location_movement_history and len(vehicle_doc.custom_vehicle_location_movement_history)>0):
        last_row= vehicle_doc.custom_vehicle_location_movement_history[-1]
        last_value= last_row.move_to
        last_odo= last_row.last_odometer
    else:
        last_value= vehicle_doc.custom_vehicle_location
        last_odo= vehicle_doc.last_odometer

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
