frappe.ui.form.on("Vehicle",{
    refresh(frm){
        
        if(!frm.is_new()){
            frm.set_df_property('custom_vehicle_location', 'read_only', 1);
        }
    }
});