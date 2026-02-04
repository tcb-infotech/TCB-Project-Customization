frappe.ui.form.on("Vehicle",{
    refresh(frm){
        
        if (!frm.is_new()) {
            frm.set_df_property("custom_vehicle_location", "read_only", 1);
            if (frappe.user.has_role("Fleet Manager")) {

                frm.add_custom_button("Reset Odometer", () => {
                    frappe.confirm(
                        `
                        <b>⚠️ WARNING: Odometer Reset</b><br><br>
                        You are about to <b>RESET the odometer</b> for this vehicle.<br><br>
                        
                        <ul>
                        <li>Vehicle mileage will be set to <b>0</b></li>
                        <li>All future mileage calculations will start fresh</li>
                        <li>Accurate mileage will be available <b>only after a FULL TANK refuelling</b></li>
                        <li>Until then, mileage data may be <b>incorrect or misleading</b></li>
                        </ul>
                        
                        <br>
                        <b>This action is NOT reversible.</b><br><br>
                        Are you sure you want to continue?
                        `,
                        () => {
                            frappe.new_doc("Vehicle Log", {
                                license_plate: frm.doc.name,
                                last_odometer: 0
                            });
                            
                            setTimeout(() => {
                                cur_frm.set_value("custom_is_odometer_reset", 1);
                            }, 300);
                        },
                        () => {
                            frappe.show_alert({
                                message: __("Odometer reset cancelled"),
                                indicator: "orange"
                            });
                        }
                    );
                },__('Actions')).addClass("btn-danger");
            }
            }
        },
        custom_vehicle_type: function(frm){
            if(frm.doc.custom_vehicle_type){
            frm.set_value('make',frm.doc.custom_vehicle_type)
        }
    },
    after_save:function(frm){
        if(frm.doc.custom_move_to_location){
            frappe.call({
                method:'tcb_project_customization.doc_events.custom_vehicle.change_vehicle_location',
                args:{
                    doc:frm.doc.name
                },
                callback:(r)=>{
                    if(r.message){
                        frm.reload_doc()
                    }
                }
            })
        }
    }
});