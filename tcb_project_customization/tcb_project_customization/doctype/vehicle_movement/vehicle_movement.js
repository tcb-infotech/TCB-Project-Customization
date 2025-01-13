frappe.ui.form.on("Vehicle Movement", {
    refresh(frm) {
        frappe.call({
            method: "tcb_project_customization.tcb_project_customization.doctype.vehicle_movement.vehicle_movement.get_records_from_vehicle_log",
            callback: (r) => {
                if (r.message) {
                    let records = r.message;
                    console.log(records)
                    
                    frm.clear_table("vehicle_movement");

                    records.forEach(record => {
                        let child = frm.add_child("vehicle_movement");
                        child.license_plate = record.license_plate;
                        child.model = record.model;
                        child.custom_current_location = record.custom_current_location;
                        child.custom_move_to = record.custom_move_to;
                        child.date = record.date;
                        child.odometer = record.odometer;
                        child.fuel_qty = record.fuel_qty;
                        child.price = record.price;
                        child.invoice = record.invoice;
                        child.employee= record.employee;
                        child.last_odometer= record.last_odometer;
                    });

                    frm.refresh_field("vehicle_movement");
                }
            }
        });
    },
});

// AT24 Medicare