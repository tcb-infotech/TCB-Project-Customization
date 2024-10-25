frappe.ui.form.on("Project",{
    refresh(frm){
        frm.set_query("supervisor_id","custom_supervisor_details", function(doc, cdt, cdn){
            return{
                "filters":{
                    "designation": "Supervisor"
                }
            }
        });

        frm.set_query("gang_leader_id","custom_gang_leader_details", function(doc, cdt, cdn){
            return{
                "filters":{
                    "designation": "Gang Leader"
                }
            }
        });
        
        frm.set_query("watchman_id","custom_watchmen_details", function(doc, cdt, cdn){
            return{
                "filters":{
                    "designation": "Watchman"
                }
            }
        });

        frm.add_custom_button(__('Add Vehicle In Project'), function() {
            let d = new frappe.ui.Dialog({
                title: 'Vehicle Assignment',
                fields: [
                    {
                        label: 'Vehicles',
                        fieldname: 'vehicle_selection_html',
                        fieldtype: 'HTML'
                    }
                ],
                primary_action_label: 'Add Selected Vehicles',
                primary_action(values) {
                    updateVehicles(frm, d);
                }
            });

            fetchAndRenderVehicles(frm, d);
            d.show();
        });
    }
});

function fetchAndRenderVehicles(frm, dialog) {
    frappe.call({
        method: 'frappe.client.get_list',
        args: {
            doctype: 'Vehicle',
            fields: ['name', 'license_plate', 'custom_project', 'last_odometer', 'make', 'custom_vehicle_movement_history'],
            order_by: 'license_plate asc'
        },
        callback: function(r) {
            let vehicles = r.message || [];
            let html = `
                <div class="vehicle-selection">
                    <div class="mb-3">
                        <button class="btn btn-xs btn-default select-all">Select All</button>
                        <button class="btn btn-xs btn-default unselect-all ml-2">Unselect All</button>
                    </div>
                    <div class="vehicle-lists">
                        <div class="in-project mb-4">
                            <h6>Vehicles In Project</h6>
                            <div class="vehicle-checkboxes d-flex flex-wrap">
                                ${vehicles
                                    .filter(v => v.custom_project === frm.doc.name)
                                    .map(vehicle => createVehicleCheckbox(vehicle, true))
                                    .join('')}
                            </div>
                        </div>
                        <div class="not-in-project">
                            <h6>Vehicles Not In Project</h6>
                            <div class="vehicle-checkboxes d-flex flex-wrap">
                                ${vehicles
                                    .filter(v => v.custom_project !== frm.doc.name)
                                    .map(vehicle => createVehicleCheckbox(vehicle, false))
                                    .join('')}
                            </div>
                        </div>
                    </div>
                </div>
            `;

            dialog.fields_dict.vehicle_selection_html.$wrapper.html(html);

            // Bind events
            dialog.$wrapper.find('.select-all').on('click', function() {
                dialog.$wrapper.find('input[type="checkbox"]').prop('checked', true);
            });

            dialog.$wrapper.find('.unselect-all').on('click', function() {
                dialog.$wrapper.find('input[type="checkbox"]').prop('checked', false);
            });
        }
    });
}

function createVehicleCheckbox(vehicle, inProject) {
    return `
        <div class="checkbox">
            <label class="ml-4">
                <input type="checkbox" 
                       data-vehicle="${vehicle.name}"
                       data-odometer="${vehicle.last_odometer || 0}"
                       data-current-project="${vehicle.custom_project || ''}"
                       ${inProject ? 'checked' : ''}>
                ${vehicle.license_plate || vehicle.name} : ${vehicle.make}
            </label>
        </div>
    `;
}

function updateVehicles(frm, dialog) {
    let promises = [];
    let currentDateTime = frappe.datetime.now_datetime();
    
    // Handle unselected vehicles (those being removed from project)
    dialog.$wrapper.find('input[type="checkbox"]:not(:checked)').each(function() {
        let $checkbox = $(this);
        let vehicleName = $checkbox.data('vehicle');
        let currentProject = $checkbox.data('current-project');

        // Only process if vehicle was previously in this project
        if (currentProject === frm.doc.name) {
            promises.push(new Promise((resolve, reject) => {
                frappe.call({
                    method: 'frappe.client.get',
                    args: {
                        doctype: 'Vehicle',
                        name: vehicleName
                    },
                    callback: function(vehicle_r) {
                        let currentVehicle = vehicle_r.message;
                        let history = currentVehicle.custom_vehicle_movement_history || [];
                        
                        // Find the latest entry for this project and update its out_date
                        let latestEntry = history.find(h => h.used_in === frm.doc.name && !h.out_date);
                        if (latestEntry) {
                            frappe.call({
                                method: 'frappe.client.set_value',
                                args: {
                                    doctype: 'Vehicle History Item',
                                    name: latestEntry.name,
                                    fieldname: 'out_date',
                                    value: currentDateTime
                                },
                                callback: function() {
                                    // Update vehicle's project field to empty
                                    frappe.call({
                                        method: 'frappe.client.set_value',
                                        args: {
                                            doctype: 'Vehicle',
                                            name: vehicleName,
                                            fieldname: 'custom_project',
                                            value: ''
                                        },
                                        callback: resolve,
                                        error: reject
                                    });
                                },
                                error: reject
                            });
                        }
                    },
                    error: reject
                });
            }));
        }
    });
    
    // Handle selected vehicles (those being added to project)
    dialog.$wrapper.find('input[type="checkbox"]:checked').each(function() {
        let $checkbox = $(this);
        let vehicleName = $checkbox.data('vehicle');
        let currentProject = $checkbox.data('current-project');
        let currentOdometer = $checkbox.data('odometer');

        // Skip if vehicle is already in this project
        if (currentProject === frm.doc.name) {
            return;
        }

        promises.push(new Promise((resolve, reject) => {
            // First handle the previous project if it exists
            let previousProjectPromise = Promise.resolve();
            if (currentProject) {
                previousProjectPromise = new Promise((res, rej) => {
                    frappe.call({
                        method: 'frappe.client.get',
                        args: {
                            doctype: 'Vehicle',
                            name: vehicleName
                        },
                        callback: function(vehicle_r) {
                            let currentVehicle = vehicle_r.message;
                            let history = currentVehicle.custom_vehicle_movement_history || [];
                            let latestEntry = history.find(h => h.used_in === currentProject && !h.out_date);
                            
                            if (latestEntry) {
                                frappe.call({
                                    method: 'frappe.client.set_value',
                                    args: {
                                        doctype: 'Vehicle History Item',
                                        name: latestEntry.name,
                                        fieldname: 'out_date',
                                        value: currentDateTime
                                    },
                                    callback: res,
                                    error: rej
                                });
                            } else {
                                res();
                            }
                        },
                        error: rej
                    });
                });
            }

            previousProjectPromise.then(() => {
                // Update vehicle's project field
                frappe.call({
                    method: 'frappe.client.set_value',
                    args: {
                        doctype: 'Vehicle',
                        name: vehicleName,
                        fieldname: 'custom_project',
                        value: frm.doc.name
                    },
                    callback: function() {
                        // Add new history entry
                        frappe.call({
                            method: 'frappe.client.insert',
                            args: {
                                doc: {
                                    doctype: 'Vehicle History Item',
                                    parent: vehicleName,
                                    parenttype: 'Vehicle',
                                    parentfield: 'custom_vehicle_movement_history',
                                    used_in: frm.doc.name,
                                    movement_date: currentDateTime,
                                    last_odometer: currentOdometer
                                }
                            },
                            callback: resolve,
                            error: reject
                        });
                    },
                    error: reject
                });
            }).catch(reject);
        }));
    });

    // Wait for all updates to complete
    Promise.all(promises)
        .then(() => {
            frappe.show_alert({
                message: __('Vehicles updated successfully'),
                indicator: 'green'
            });
            dialog.hide();
            frm.reload_doc();
        })
        .catch((err) => {
            frappe.show_alert({
                message: __('Error updating vehicles'),
                indicator: 'red'
            });
            console.error(err);
        });
}