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


		if (frm.is_new()) {
            frm.clear_table('time_logs');
            frm.refresh_field('time_logs');
        }

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
								reqd: 1
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
