// Copyright (c) 2024, AjayRaj Mahiwal and contributors
// For license information, please see license.txt

frappe.ui.form.on("Direct Timesheet", {
	refresh(frm) {
        frm.set_query("gang_leader","time_logs", function(doc,cdt,cdn){
			return{
				"filters": {
					"designation":"Gang Leader"
				}
			}
		});
		frm.set_query("supervisor_id","supervisor_details", function(doc, cdt, cdn){
            return{
                "filters":{
                    "designation": "Supervisor"
                }
            }
        });

        frm.set_query("gang_leader_id","gang_leader_details", function(doc, cdt, cdn){
            return{
                "filters":{
                    "designation": "Gang Leader"
                }
            }
        });
        
        frm.set_query("watchman_id","watchmen_details", function(doc, cdt, cdn){
            return{
                "filters":{
                    "designation": "Watchman"
                }
            }
        });

		if(!frm.is_new()){
			frm.add_custom_button(__('Sync Project Details'), function() {
				get_project_details(frm);
			}, __('Actions'));
		}


		// if (frm.is_new()) {
        //     frm.clear_table('time_logs');
        //     frm.refresh_field('time_logs');
        // }

		if(frm.doc.docstatus == 0){
		frm.add_custom_button(__('Fill Timesheet'), function() {
			let d = new frappe.ui.Dialog({
						title: 'Enter Timesheet Details',
						fields: [
							{
								label: 'Gang Leader',
								fieldname: 'gang_leader',
								fieldtype: 'Link',
								options: 'Employee',
								reqd: 1,
								get_query: function() {
									return {
										filters: {
											"designation": "Gang Leader"
										}
									};
								}
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
								label: 'From Time',
								fieldname: 'from_time',
								fieldtype: 'Datetime',
								reqd: 1
							},
							{
								"fieldname": "column_break_jqjq",
								"fieldtype": "Column Break"
							},
							{
								label: 'To Time',
								fieldname: 'to_time',
								fieldtype: 'Datetime',
								reqd: 1
							},
							{
								fieldname: 'section_break_2',
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
							let from_time = moment(values.from_time);
							let to_time = moment(values.to_time);
							let hours = moment.duration(to_time.diff(from_time)).asHours();
		
							frm.add_child('time_logs', {
								gang_leader: values.gang_leader,
								activity_type: values.activity_type,
								task: values.task,
								from_time: values.from_time,
								to_time: values.to_time,
								description: values.description,
								hours: hours,
							});
		
							frm.refresh_field('time_logs');
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
			frm.doc.supervisor_details = []
			frm.doc.gang_leader_details = []
			frm.doc.watchmen_details = []

			frm.refresh_field('supervisor_details');
			frm.refresh_field('gang_leader_details');
			frm.refresh_field('watchmen_details');
		}
    },

});

frappe.ui.form.on("Direct Timesheet Item",{
    from_time: function (frm, cdt, cdn) {
        calculate_end_time(frm, cdt, cdn);
    },
    to_time: function (frm, cdt, cdn) {
        var child = locals[cdt][cdn];

        if (frm._setting_hours) return;

        var hours = moment(child.to_time).diff(moment(child.from_time), "seconds") / 3600;
        frappe.model.set_value(cdt, cdn, "hours", hours);
    }
})

var calculate_end_time = function (frm, cdt, cdn) {
	let child = locals[cdt][cdn];

	if (!child.from_time) {
		frappe.model.set_value(cdt, cdn, "from_time", frappe.datetime.get_datetime_as_string());
	}

	let d = moment(child.from_time);
	if (child.hours) {
		d.add(child.hours, "hours");
		frm._setting_hours = true;
		frappe.model.set_value(cdt, cdn, "to_time", d.format(frappe.defaultDatetimeFormat)).then(() => {
			frm._setting_hours = false;
		});
	}
};


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