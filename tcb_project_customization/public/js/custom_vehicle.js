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