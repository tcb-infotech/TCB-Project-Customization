// Client-side JavaScript
frappe.ui.form.on('Vehicle Log', {
    // onload: function(frm){
    //     (frm.doc.license_plate){
    //         frappe.call({
    //             method:'tcb_project_customization.doc_events.custom_vehicle_log.set_current_location',
    //             args:{
    //                 license_plate:frm.doc.license_plate,
    //             },
    //             callback:(r)=>{
    //                 if(r.message){
    //                     frm.set_value('custom_current_location',r.message.location)
    //                     frm.set_value('last_odometer',r.message.odometer)
    //                 }
    //             }
    //         })if
    //     }
    // },

    refresh: function(frm) {
        // if (frm.doc.custom_current_location) {
        //     frm.set_df_property('custom_current_location', 'read_only', 1);
        // }
        if(frm.doc.custom_current_location){
            frm.set_query('custom_move_to', ()=>{
                return {
                    "filters" : {
                        "location_name": frm.doc.custom_current_location,
                    }
                }
            })
        }
    },

    license_plate: function(frm){
        frm.set_value('custom_move_to',"");
    },
    custom_current_location: function(frm){
        frm.set_query('custom_move_to', ()=>{
            return {
                "filters" : {
                    "location_name": ["!=", frm.doc.custom_current_location],
                }
            }
        })
    },

    before_save: function(frm) {
        frappe.call({
            method: 'tcb_project_customization.doc_events.custom_vehicle_log.get_draft_entries',
            args: {
                doc: frm.doc
            },
            callback: (r) => {
                if (Array.isArray(r.message) && r.message.length > 0) {  
                    frappe.validated = false; 
                    
                    frappe.confirm(
                        'You cannot submit as there are pending draft entries. Would you like to be redirected to them?',
                        function() {
                            frappe.set_route('List', 'Vehicle Log', {
                                license_plate: frm.doc.license_plate,
                                docstatus: ["!=", 1]
                            });
                        },
                        function() {
                            // If user clicks "No", just stay on the current document
                            // Do nothing, just keep on the current form
                        }
                    );
                } else {
                    console.log("No draft entries found");
                }
            }
        });
    },
    
    
    after_save: function(frm) { 
        if(frm.doc.docstatus==1){
            if (frm.doc.custom_move_to) {
                frappe.call({
                    method: 'tcb_project_customization.doc_events.custom_vehicle_log.set_vehicle_movement',
                    args: {
                        doc: frm.doc
                    }
                });
            }
        }
    }
});

