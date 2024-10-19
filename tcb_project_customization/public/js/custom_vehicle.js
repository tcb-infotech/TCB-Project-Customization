frappe.ui.form.on("Vehicle",{
    refresh(frm){
        frm.add_custom_button(__("Move Vehicle"), function(){
            let d = new frappe.ui.Dialog({
                title: 'Vehicle Movement ',
                fields:[
                    {
                        label: "Current Location",
                        fieldname: "move_from",
                        fieldtype: "Link",
                        options: "Project",
                        default: frm.doc.custom_project || "",
                        read_only: 1,
                    },
                    {
                        "fieldname": "column_break_1",
                        "fieldtype": "Column Break"
                    },
                    {
                        fieldname: "move_from_project_name",
                        fieldtype: "Data",
                        label: "Project Name",
                        default: frm.doc.custom_project_name,
                        read_only: 1
                    },
                    {
                        "fieldname": "section_break_1",
                        "fieldtype": "Section Break"
                    },
                    {
                        label: "Move To",
                        fieldname: "move_to",
                        fieldtype: "Link",
                        options: "Project",
                        reqd: 1,
                        onchange: function() {
                            if(this.value) {
                                frappe.db.get_value('Project', this.value, 'project_name')
                                    .then(r => {
                                        if(r.message) {
                                            d.set_value('move_to_project_name', r.message.project_name);
                                        }
                                    });
                            }
                        }
                    },
                    {
                        "fieldname": "column_break_2",
                        "fieldtype": "Column Break"
                    },
                    {
                        fieldname: "move_to_project_name",
                        fieldtype: "Data",
                        label: "Project Name",
                        read_only: 1
                    },
                    // {
                    //     "fieldname": "section_break_2",
                    //     "fieldtype": "Section Break"
                    // },
                    
                ],
						primary_action_label: 'Save',
						primary_action(values) {
                            let d1 = frappe.msgprint({
                                title: __("Confirmation"),
                                message: __(
                                  `Are you sure you want to move Vehicle from ${values.move_from_project_name || 'None'} to ${values.move_to_project_name}?`
                                ),
                                primary_action: {
                                  label: "Proceed",
                                  action: function () {
                                    move_vehicle(frm, values);
                                    d1.hide();
                                        // frm.add_child('vehicle_movement_history', {
                                        // });
                    
                                        // frm.refresh_field('vehicle_movement_history');
                                        d.hide();
                                        frappe.show_alert({
                                            message: __(`Vehicle moved to ${values.move_to_project_name} successfully`),
                                            indicator: 'green'
                                        });

                                        frm.save();
                                  },
                                },
                              });
                            
						}
            });
            d.show();
        })
    }
});





function move_vehicle(frm, values) {
	try {
	  let new_row = frappe.model.add_child(
		frm.doc,
		"Vehicle History Item",
		"custom_vehicle_movement_history"
	  );
  
	  console.log(frappe.datetime.now_datetime());
  
	  let movement_date_value = frappe.datetime.now_datetime();
  
	  // Set values in the new row
	  frappe.model.set_value(new_row.doctype, new_row.name, {
        movement_date: movement_date_value,
        move_from: values.move_from,
        move_to: values.move_to,
	  });
  
	  // Refresh the child table
	  frm.refresh_field("custom_vehicle_movement_history");

      frm.set_value('custom_project', values.move_to);
	  
	  frm.save();
	} catch (e) {
	  frappe.throw("Not able to Move Vehicle due to some technical issue.")
	}
  }