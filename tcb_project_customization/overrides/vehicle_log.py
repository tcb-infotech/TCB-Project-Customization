import frappe
from frappe.model.document import Document
from frappe.utils import flt

class VehicleLog(Document):

    def validate(self):
        if self.custom_is_odometer_reset:
            return  
        
        if flt(self.odometer) < flt(self.last_odometer):
            frappe.throw(
                f"Current Odometer Value should be greater than Last Odometer Value {self.last_odometer}"
            )
            
    def on_submit(self):
        if self.custom_is_odometer_reset:
            frappe.db.set_value("Vehicle", self.license_plate, "custom_vehicle_mileage", "Odometer Rest! Mileage will be available after next full refuel")
            vehicle_doc = frappe.get_doc("Vehicle", self.license_plate)
            vehicle_doc.add_comment(
                "Comment",
                "⚠️ Odometer Reset: "
                "The odometer of this vehicle was reset. Mileage calculations will be accurate only after the vehicle is refuelled with a FULL TANK."
            )
        frappe.db.set_value("Vehicle", self.license_plate, "last_odometer", self.odometer)

    def on_cancel(self):
        distance_travelled = self.odometer - self.last_odometer
        if distance_travelled > 0:
            updated_odometer_value = (
                int(frappe.db.get_value("Vehicle", self.license_plate, "last_odometer")) - distance_travelled
            )
            frappe.db.set_value("Vehicle", self.license_plate, "last_odometer", updated_odometer_value)

