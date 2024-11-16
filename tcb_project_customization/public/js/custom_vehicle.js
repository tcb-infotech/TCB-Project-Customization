frappe.ui.form.on("Vehicle",{
    refresh(frm){
        
        if(!frm.is_new()){
            frm.set_df_property('custom_vehicle_location', 'read_only', 1);
        }
    },
    custom_vehicle_type: function(frm){
        if(frm.doc.custom_vehicle_type){
            frm.set_value('make',frm.doc.custom_vehicle_type)
        }
    }
});