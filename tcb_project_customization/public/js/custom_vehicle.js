// frappe.ui.form.on("Vehicle",{
//     refresh(frm){
        
//         if(!frm.is_new()){
//             frm.set_df_property('custom_vehicle_location', 'read_only', 1);
//         }

//         frm.add_custom_button(__("Move Vehicle"), function(){
//             let d = new frappe.ui.Dialog({
//                 title: 'Where you want to move ?',
//                 fields:[
//                     {
//                         label: "Current Location",
//                         fieldname: "move_from",
//                         fieldtype: "Data",
//                         default: frm.doc.custom_vehicle_location || "Initial",
//                         read_only:1,
//                     },
//                     {
//                         "fieldname": "column_break_1",
//                         "fieldtype": "Column Break"
//                     },
                
//                     // {
//                     //     "fieldname": "section_break_1",
//                     //     "fieldtype": "Section Break"
//                     // },
//                     {
//                         label: "Move To",
//                         fieldname: "move_to",
//                         fieldtype: "Link",
//                         options: "Location",
//                         reqd: 1,
//                     },
                    
//                 ],
//                         primary_action_label: 'Save',
//                         primary_action(values) {
//                             let d1 = frappe.msgprint({
//                                 title: __("Confirmation"),
//                                 message: __(
//                                   `Are you sure you want to move Vehicle from ${values.move_from || 'Inital'} to ${values.move_to} Location?`
//                                 ),
//                                 primary_action: {
//                                   label: "Proceed",
//                                   action: function () {
//                                     values.cdt_name = "Vehicle Location History Item"
//                                     values.dt_table_name = "custom_vehicle_location_movement_history"
//                                     values.dt_field_name = "custom_vehicle_location"
//                                     move_vehicle(frm, values);
//                                     d1.hide();
//                                         // frm.add_child('vehicle_movement_history', {
//                                         // });
                    
//                                         // frm.refresh_field('vehicle_movement_history');
//                                         d.hide();
//                                         frappe.show_alert({
//                                             message: __(`Vehicle moved to ${values.move_to} location successfully`),
//                                             indicator: 'green'
//                                         });

//                                         frm.save();
//                                   },
//                                 },
//                               });
                            
//                         }
//             });
//             d.show();

            // let dialog_decider = new frappe.ui.Dialog({
            //     title: 'Where you want to move ?',
            //     fields:[
            //         {
            //             label:"Move To",
            //             fieldname:"vehicle_move_to",
            //             fieldtype: "Data",
            //             // fieldtype: "Select",
            //             default:"Location",
            //             // options:"Location\nProject",
            //             reqd:1,
            //         },
            //     ],
            //     primary_action_label: 'Load',
            //     primary_action(values){
            //              dialog_decider.hide();
            //             if(values.vehicle_move_to == 'Project'){
            //                 let d = new frappe.ui.Dialog({
            //                     title: 'Vehicle Movement: Project',
            //                     fields:[
            //                         {
            //                             label: "Current Project",
            //                             fieldname: "move_from",
            //                             fieldtype: "Link",
            //                             options: "Project",
            //                             default: frm.doc.custom_project || "Initial",
            //                             read_only: 1,
            //                         },
            //                         {
            //                             "fieldname": "column_break_1",
            //                             "fieldtype": "Column Break"
            //                         },
            //                         {
            //                             fieldname: "move_from_project_name",
            //                             fieldtype: "Data",
            //                             label: "Project Name",
            //                             default: frm.doc.custom_project_name || "Initial",
            //                             read_only: 1
            //                         },
            //                         {
            //                             "fieldname": "section_break_1",
            //                             "fieldtype": "Section Break"
            //                         },
            //                         {
            //                             label: "Move To",
            //                             fieldname: "move_to",
            //                             fieldtype: "Link",
            //                             options: "Project",
            //                             reqd: 1,
            //                             onchange: function() {
            //                                 if(this.value) {
            //                                     frappe.db.get_value('Project', this.value, 'project_name')
            //                                         .then(r => {
            //                                             if(r.message) {
            //                                                 d.set_value('move_to_project_name', r.message.project_name);
            //                                             }
            //                                         });
            //                                 }
            //                             }
            //                         },
            //                         {
            //                             "fieldname": "column_break_2",
            //                             "fieldtype": "Column Break"
            //                         },
            //                         {
            //                             fieldname: "move_to_project_name",
            //                             fieldtype: "Data",
            //                             label: "Project Name",
            //                             read_only: 1
            //                         },
            //                         // {
            //                         //     "fieldname": "section_break_2",
            //                         //     "fieldtype": "Section Break"
            //                         // },
                                    
            //                     ],
            //                             primary_action_label: 'Save',
            //                             primary_action(values) {
            //                                 let d1 = frappe.msgprint({
            //                                     title: __("Confirmation"),
            //                                     message: __(
            //                                       `Are you sure you want to move Vehicle from ${values.move_from_project_name || 'Inital'} to ${values.move_to_project_name} Project?`
            //                                     ),
            //                                     primary_action: {
            //                                       label: "Proceed",
            //                                       action: function () {
            //                                         values.cdt_name = "Vehicle History Item"
            //                                         values.dt_table_name = "custom_vehicle_movement_history"
            //                                         values.dt_field_name = "custom_project"
            //                                         move_vehicle(frm, values);
            //                                         d1.hide();
            //                                             // frm.add_child('vehicle_movement_history', {
            //                                             // });
                                    
            //                                             // frm.refresh_field('vehicle_movement_history');
            //                                             d.hide();
            //                                             frappe.show_alert({
            //                                                 message: __(`Vehicle moved to ${values.move_to_project_name} project successfully`),
            //                                                 indicator: 'green'
            //                                             });
                
            //                                             frm.save();
            //                                       },
            //                                     },
            //                                   });
                                            
            //                             }
            //                 });
            //                 d.show();
            //             }
            //             else{
            //                 let d = new frappe.ui.Dialog({
            //                     title: 'Vehicle Movement: Location',
            //                     fields:[
            //                         {
            //                             label: "Current Location",
            //                             fieldname: "move_from",
            //                             fieldtype: "Data",
            //                             default: frm.doc.custom_vehicle_location || "Initial",
            //                             read_only:1,
            //                         },
            //                         {
            //                             "fieldname": "column_break_1",
            //                             "fieldtype": "Column Break"
            //                         },
                                
            //                         // {
            //                         //     "fieldname": "section_break_1",
            //                         //     "fieldtype": "Section Break"
            //                         // },
            //                         {
            //                             label: "Move To",
            //                             fieldname: "move_to",
            //                             fieldtype: "Link",
            //                             options: "Location",
            //                             reqd: 1,
            //                         },
                                    
            //                     ],
            //                             primary_action_label: 'Save',
            //                             primary_action(values) {
            //                                 let d1 = frappe.msgprint({
            //                                     title: __("Confirmation"),
            //                                     message: __(
            //                                       `Are you sure you want to move Vehicle from ${values.move_from || 'Inital'} to ${values.move_to} Location?`
            //                                     ),
            //                                     primary_action: {
            //                                       label: "Proceed",
            //                                       action: function () {
            //                                         values.cdt_name = "Vehicle Location History Item"
            //                                         values.dt_table_name = "custom_vehicle_location_movement_history"
            //                                         values.dt_field_name = "custom_vehicle_location"
            //                                         move_vehicle(frm, values);
            //                                         d1.hide();
            //                                             // frm.add_child('vehicle_movement_history', {
            //                                             // });
                                    
            //                                             // frm.refresh_field('vehicle_movement_history');
            //                                             d.hide();
            //                                             frappe.show_alert({
            //                                                 message: __(`Vehicle moved to ${values.move_to} location successfully`),
            //                                                 indicator: 'green'
            //                                             });
                
            //                                             frm.save();
            //                                       },
            //                                     },
            //                                   });
                                            
            //                             }
            //                 });
            //                 d.show();
            //             }


            //     }
            // });

            // dialog_decider.show();
            
//         })
//     }
// });





// function move_vehicle(frm, values) {
// 	try {
// 	  let new_row = frappe.model.add_child(
// 		frm.doc,
// 		values.cdt_name,
//         values.dt_table_name
// 	  );
  
  
// 	  let movement_date_value = frappe.datetime.now_datetime();
  
// 	  // Set values in the new row
// 	  frappe.model.set_value(new_row.doctype, new_row.name, {
//         movement_date: movement_date_value,
//         move_from: values.move_from || "Initial",
//         move_to: values.move_to,
//         last_odometer: frm.doc.last_odometer
// 	  });
  
// 	  // Refresh the child table
// 	  frm.refresh_field(values.dt_table_name);

//       frm.set_value(values.dt_field_name, values.move_to);
	  
// 	  frm.save();
// 	} catch (e) {
// 	  frappe.throw("Not able to Move Vehicle due to some technical issue.")
// 	}
//   }




frappe.ui.form.on('Vehicle',{
  refresh: function(frm){
    if(frm.doc.custom_vehicle_location_movement_history && frm.doc.custom_vehicle_location_movement_history.length>0){
      let last_row= frm.doc.custom_vehicle_location_movement_history[frm.doc.custom_vehicle_location_movement_history.length-1]
      let last_value= last_row.move_to

      frm.set_value('custom_vehicle_location',last_value)
      frm.save()
  }
  }
})