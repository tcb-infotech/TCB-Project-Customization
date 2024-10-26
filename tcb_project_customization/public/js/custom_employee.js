frappe.ui.form.on("Employee", {
    refresh(frm) {
        frm.add_custom_button("Add Internal", () => {
            let d = new frappe.ui.Dialog({
                'title': 'Update Internal Work History',
                fields: [
                    {
                        label: 'Project',
                        fieldname: 'working_on_project',
                        fieldtype: "Link",
                        options: "Project",
                        description: "(Current Working On)",
                        read_only: 1,
                        default: frm.doc.custom_project
                    },
                    {
                        fieldname: "col-1",
                        fieldtype: "Column Break"
                    },
                    {
                        label: 'Transfer To',
                        fieldname: 'new_project',
                        fieldtype: "Link",
                        options: "Project",
                        reqd: 1,
                    }
                ],
                primary_action_label: 'Transfer',
                primary_action(values) {

                    transfer_emp(frm, values).then(()=>{
                        d.hide();
                    })
                }
            })

            d.show();
        });
    }
});

function transfer_emp(frm, values) {
    let history = frm.doc.internal_work_history || [];
    let currentDateTime = frappe.datetime.now_datetime();


    let lastHistoryEntry = history.find(h => h.custom_project === frm.doc.custom_project && !h.to_date);
    if (lastHistoryEntry) {
        frappe.call({
            method: 'frappe.client.set_value',
            args: {
                doctype: 'Employee Internal Work History',
                name: lastHistoryEntry.name,
                fieldname: 'to_date',
                value: currentDateTime
            },
            callback: function () {
                add_new_work_history(frm, values);
            },
        });
    } 
    else {
        add_new_work_history(frm, values);
    }

    return Promise.resolve();
    
}

function add_new_work_history(frm, values){

    frm.set_value('custom_project', values.new_project);

    frm.add_child('internal_work_history', {
        custom_project: values.new_project,
        designation: frm.doc.designation,
        from_date: frappe.datetime.now_datetime(),
        branch: frm.doc.branch,
        department: frm.doc.department
    });

    frm.refresh_field('internal_work_history');
    frappe.show_alert({
        message: __('Transfer entry added successfully in work history !'),
        indicator: 'green'
    });

    frm.save();
}