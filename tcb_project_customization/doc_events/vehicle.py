import frappe



def calculate_vehicle_mileage(doc, method=None):
    # doc = frappe.get_doc("Vehicle Log")
    # if not doc.docstatus == 0:
    refuel_logs = frappe.db.get_all(
        "Vehicle Log",
        filters={"license_plate": doc.license_plate, "fuel_qty" : [">", 0]},
        fields=["*"],
        order_by="creation desc",
        limit=2
    )
    if len(refuel_logs) < 2:
        # not enough logs to compute mileage
        frappe.db.set_value('Vehicle', doc.license_plate, {'custom_vehicle_mileage':"Vehicle Not Refueled Yet!"} , update_modified=False)
        return
    
    refuel_log_1 = refuel_logs[0]
    refuel_log_2 = refuel_logs[1]
    
    # print('-----this is refuel log ----',refuel_log_1)
    # print('-----this is refuel log ----',refuel_log_2)
    
    # print('-----this is refuel log ----',refuel_log_1.odometer - refuel_log_2.odometer)
    # print('-----this is refuel log ----',(refuel_log_1.odometer - refuel_log_2.odometer)/refuel_log_2.fuel_qty)
    vehicle_mileage = (refuel_log_1.odometer - refuel_log_2.odometer)/refuel_log_2.fuel_qty
    # related_vehicle_doc = frappe.get_doc('Vehicle',doc.license_plate)
    
    # frappe.db.set_value()
    
    frappe.db.set_value('Vehicle', doc.license_plate, {'custom_vehicle_mileage':vehicle_mileage} , update_modified=False)
    # after_refuel_logs = frappe.db.get_all(
    #     "Vehicle Log",
    #     filters={"license_plate": doc.license_plate, "creation" : [">", refuel_log_1.creation]},
    #     fields=["*"],
    #     order_by="creation desc",
    #     # limit=1
    # )
    
    # print('-----this is after refuel log ----',after_refuel_logs)
    # print('npppppppp-------doc --',doc)
        # log = 
        
        # custom_last_date
        
@frappe.whitelist()
def set_all_vehicles_mileage():
    """
    One-time run: compute and set custom_vehicle_mileage for all Vehicles.
    Returns dict with summary.
    """
    vehicles = frappe.get_all("Vehicle", fields=["name"])
    total = len(vehicles)
    updated = 0
    errors = 0

    for v in vehicles:
        vehicle_name = v.get("name")
        try:
            refuel_logs = frappe.get_all(
                "Vehicle Log",
                filters={"license_plate": vehicle_name, "fuel_qty": [">", 0]},
                fields=["odometer", "fuel_qty", "name", "creation"],
                order_by="creation desc",
                limit=2
            )

            if len(refuel_logs) < 2:
                frappe.db.set_value('Vehicle', vehicle_name, {'custom_vehicle_mileage':"Vehicle Not Refueled Yet!"} , update_modified=False)
                # not enough logs to compute mileage
                continue

            r1, r2 = refuel_logs[0], refuel_logs[1]

            # validate numeric values
            od1 = r1.get("odometer") or 0
            od2 = r2.get("odometer") or 0
            fuel = r2.get("fuel_qty") or 0

            # basic sanity checks
            distance = od1 - od2
            if fuel <= 0 or distance <= 0:
                # invalid values — skip
                continue

            mileage = distance / float(fuel)

            # write value without updating modified timestamp
            frappe.db.set_value("Vehicle", vehicle_name, "custom_vehicle_mileage", mileage, update_modified=False)
            updated += 1

        except Exception as e:
            errors += 1
            # log error to error log in bench
            frappe.log_error(message=frappe.get_traceback(), title=f"Vehicle mileage update: {vehicle_name}")

    # commit once
    frappe.db.commit()

    print( {"total_vehicles": total, "updated": updated, "errors": errors})