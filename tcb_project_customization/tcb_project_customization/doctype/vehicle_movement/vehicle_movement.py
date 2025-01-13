# Copyright (c) 2025, AjayRaj Mahiwal and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class VehicleMovement(Document):
	pass


@frappe.whitelist()
def get_records_from_vehicle_log():
    try:
        records = frappe.get_all("Vehicle Log", fields=[
            "license_plate", "model", "custom_current_location", "custom_move_to",
            "date", "odometer", "fuel_qty", "price", "invoice","employee","last_odometer"
        ])
        return records
    except Exception as e:
        frappe.throw(str(e))
