// Copyright (c) 2024, AjayRaj Mahiwal and contributors
// For license information, please see license.txt

frappe.ui.form.on("Direct Timesheet", {
	refresh(frm) {
        // frm.set_query("gang_leader","staff_details", function(doc,cdt,cdn){
		// 	return{
		// 		"filters": {
		// 			"designation":"Gang Leader"
		// 		}
		// 	}
		// });
		// frm.set_query("supervisor_id","supervisor_details", function(doc, cdt, cdn){
        //     return{
        //         "filters":{
        //             "designation": "Supervisor"
        //         }
        //     }
        // });

        // frm.set_query("gang_leader_id","gang_leader_details", function(doc, cdt, cdn){
        //     return{
        //         "filters":{
        //             "designation": "Gang Leader"
        //         }
        //     }
        // });
        
        // frm.set_query("watchman_id","watchmen_details", function(doc, cdt, cdn){
        //     return{
        //         "filters":{
        //             "designation": "Watchman"
        //         }
        //     }
        // });

		if(!frm.is_new()){
			frm.add_custom_button(__('Sync Project Details'), function() {
				get_project_details(frm);
			}, __('Actions'));
		}


		// if (frm.is_new()) {
        //     frm.clear_table('staff_details');
        //     frm.refresh_field('staff_details');
        // }

		if(frm.doc.docstatus == 0){
		frm.add_custom_button(__('Fill Timesheet'), function() {
			let d = new frappe.ui.Dialog({
						title: 'Enter Timesheet Details',
						fields: [
							{
								label: 'Employee',
								fieldname: 'employee',
								fieldtype: 'Link',
								options: 'Employee',
								reqd: 1,
							},
							{
								label: 'Activity Type',
								fieldname: 'activity_type',
								fieldtype: 'Link',
								options: 'Activity Type'
							},
							{
								label: 'Task',
								fieldname: 'task',
								fieldtype: 'Link',
								options: 'Task'
							},
							{
								fieldname: 'section_break_1',
								fieldtype: 'Section Break',
							},
							{
								label: 'Description',
								fieldname: 'description',
								fieldtype: 'Small Text',
							}
						],
						size:'large',
						primary_action_label: 'Save',
						primary_action(values) {
		
							frm.add_child('staff_details', {
								employee: values.employee,
								activity_type: values.activity_type,
								task: values.task,
								description: values.description,
							});
		
							frm.refresh_field('staff_details');
							d.hide();
							frappe.show_alert({
								message: __('Timesheet entry added successfully'),
								indicator: 'green'
							});
						}
					});

			d.show();
		});
	}
	},
	project: function(frm) {
        if (frm.doc.project && !frm.is_new()) {
			get_project_details(frm);
        }else{
			frm.doc.staff_details = []

			frm.refresh_field('staff_details');
		}
    },

});



function get_project_details(frm){
	if (frm.doc.project) {
		frm.call({
			method: 'tcb_project_customization.tcb_project_customization.doctype.direct_timesheet.direct_timesheet.sync_project_details_with_timesheet',
			args: {
				timesheet_id: frm.doc.name,
				project: frm.doc.project
			},
			freeze: true,
			freeze_message: __('Syncing Project Details...'),
			callback: function(r) {
				if (!r.exc) {
					frm.refresh();
					frm.reload_doc();
					frappe.show_alert({
						message: __('Project details synced successfully'),
						indicator: 'green'
					});
				}
			}
		});
	} else {
		frappe.throw(__('Please select a project first'));
	}
}