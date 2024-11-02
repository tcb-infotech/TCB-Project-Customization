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
                    transfer_emp(frm, values).then(() => {
                        d.hide();
                    }).catch((err) => {
                        frappe.throw(err);
                    });
                }
            })
            
            d.show();
        });
    }
});

function transfer_emp(frm, values) {
    let history = frm.doc.internal_work_history || [];
    let currentDateTime = frappe.datetime.now_datetime();
    
    return new Promise((resolve, reject) => {
        // First update supervisor details in both projects
        update_supervisor_details(frm, values)
            .then(() => {
                // Reload the form to get fresh data
                return frm.reload_doc();
            })
            .then(() => {
                // After reload, find the history entry again
                history = frm.doc.internal_work_history || [];
                let lastHistoryEntry = history.find(h => h.custom_project === frm.doc.custom_project && !h.to_date);
                
                if (lastHistoryEntry) {
                    return frappe.call({
                        method: 'frappe.client.set_value',
                        args: {
                            doctype: 'Employee Internal Work History',
                            name: lastHistoryEntry.name,
                            fieldname: 'to_date',
                            value: currentDateTime
                        }
                    });
                }
            })
            .then(() => {
                // Reload again before making new changes
                return frm.reload_doc();
            })
            .then(() => {
                return add_new_work_history(frm, values);
            })
            .then(() => {
                resolve();
            })
            .catch((err) => {
                reject('Error during transfer: ' + err);
            });
    });
}

function update_supervisor_details(frm, values) {
    return new Promise((resolve, reject) => {
        frappe.db.get_doc('Project', values.working_on_project)
            .then(old_project => {
                return frappe.db.get_doc('Project', values.new_project)
                    .then(new_project => {
                        return { old_project, new_project };
                    });
            })
            .then(({ old_project, new_project }) => {
                // Remove employee from old project's supervisor details
                if (old_project.custom_supervisor_details) {
                    old_project.custom_supervisor_details = old_project.custom_supervisor_details.filter(
                        row => row.supervisor_id !== frm.doc.name
                    );
                }

                // Add employee to new project's supervisor details
                if (!new_project.custom_supervisor_details) {
                    new_project.custom_supervisor_details = [];
                }
                
                new_project.custom_supervisor_details.push({
                    supervisor_id: frm.doc.name,
                    user_name: frm.doc.employee_name,
                });

                // Save both projects
                return Promise.all([
                    frappe.call({
                        method: 'frappe.client.save',
                        args: {
                            doc: old_project
                        }
                    }),
                    frappe.call({
                        method: 'frappe.client.save',
                        args: {
                            doc: new_project
                        }
                    })
                ]);
            })
            .then(() => {
                resolve();
            })
            .catch(err => {
                reject(err);
            });
    });
}

function add_new_work_history(frm, values) {
    return new Promise((resolve, reject) => {
        try {
            frm.set_value('custom_project', values.new_project);
            
            frm.add_child('internal_work_history', {
                custom_project: values.new_project,
                designation: frm.doc.designation,
                from_date: frappe.datetime.now_datetime(),
                branch: frm.doc.branch,
                department: frm.doc.department
            });
            
            frm.refresh_field('internal_work_history');
            
            // Save with async/await and handle the promise
            frm.save()
                .then(() => {
                    frappe.show_alert({
                        message: __('Transfer entry added successfully in work history !'),
                        indicator: 'green'
                    });
                    resolve();
                })
                .catch((err) => {
                    reject(err);
                });
        } catch (err) {
            reject(err);
        }
    });
}