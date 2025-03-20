frappe.ui.form.on("Rent", {
    refresh(frm) {
        frm.doc.table_zjnd.forEach((e) => {
            e.quantity && e.rateuom
                ? (e.total_amount =
                    e.quantity * e.rateuom +
                    (e.interest_rate / 100) * e.quantity * e.rateuom)
                : "";
        });
        frm.refresh_field("table_zjnd");

        frm.add_custom_button("Rent Management Report", function () {
            frappe.set_route("query-report", "Rent Management Report");
        });
    },

    validate: async function (frm) {
        if (!frm.doc.table_zjnd) return;

        // Handle new rent creation
        if (!frm.doc.delivery_note) {
            // Set UOMs for items
            for (const row of frm.doc.table_zjnd) {
                if (!row.uom && row.rent_item && row.document_type == "Item") {
                    await new Promise((resolve) => {
                        frappe.call({
                            method: "frappe.client.get_value",
                            args: {
                                doctype: "Item",
                                filters: { name: row.rent_item },
                                fieldname: "stock_uom",
                            },
                            callback: (r) => {
                                if (r.message && r.message.stock_uom) {
                                    frappe.model.set_value(
                                        row.doctype,
                                        row.name,
                                        "uom",
                                        r.message.stock_uom
                                    );
                                }
                                resolve();
                            },
                        });
                    });
                }
            }

            // Create delivery notes
            for (const row of frm.doc.table_zjnd) {
                if (row.warehouse && row.rent_item && row.quantity) {
                    await new Promise((resolve) => {
                        frappe.call({
                            method: "tcb_project_customization.tcb_project_customization.doctype.rent.rent.makeStockEntry",
                            args: {
                                customer: frm.doc.customer,
                                rentItem: row.rent_item,
                                warehouse: row.warehouse,
                                quantity: row.quantity,
                                rateuom: row.rateuom,
                                uom: row.uom,
                            },
                            callback: (r) => {
                                if (r.message) {
                                    frappe.msgprint("Delivery Note Created " + r.message);
                                    frm.set_value("delivery_note", r.message);
                                    resolve();
                                } else {
                                    frappe.msgprint("Some error occurred");
                                    resolve();
                                }
                            },
                        });
                    });
                }
            }
        }

        // Handle vehicles 
        let vehicleRows = frm.doc.table_zjnd.filter(row => 
            row.document_type === "Vehicle" && 
            row.rent_item && 
            row.quantity && 
            row.rateuom &&
            (!row.vehicle_processed) 
        );

        for (const row of vehicleRows) {
            frappe.show_alert("Processing vehicle: " + row.rent_item);
            await new Promise((resolve) => {
                frappe.call({
                    method: "frappe.client.set_value",
                    args: {
                        doctype: "Vehicle",
                        name: row.rent_item,
                        fieldname: "custom_status",
                        value: "Disabled",
                    },
                    callback: (r) => {
                        if (r.message) {
                            frappe.show_alert("Vehicle status updated: " + row.rent_item);
                            frappe.model.set_value(row.doctype, row.name, 'vehicle_processed', 1);
                        }
                        resolve();
                    }
                });
            });
        }

        // Handle returns
        if (frm.doc.delivery_note) {
            let returnRows = frm.doc.table_zjnd.filter(row => 
                row.document_type === "Item" && 
                row.rent_item && 
                row.quantity && 
                row.rateuom && 
                row.returned_quantity && 
                row.return_to &&
                (!row.return_processed)
            );

            if (returnRows.length > 0) {
                frappe.show_alert("Processing returns...");
                let returnDetails = returnRows.map(row => ({
                    item_code: row.rent_item,
                    returned_quantity: row.returned_quantity,
                    return_to: row.return_to
                }));

                await new Promise((resolve) => {
                    frappe.call({
                        method: "tcb_project_customization.tcb_project_customization.doctype.rent.rent.returnStockEntry",
                        args: {
                            dname: frm.doc.delivery_note,
                            return_details: returnDetails
                        },
                        callback: function (r) {
                            if (r.message) {
                                frappe.msgprint({
                                    title: 'Return Note Created',
                                    message: `Return Delivery Note Created: <b>${r.message}</b>`,
                                    indicator: 'green'
                                });
                                // Mark returns as processed
                                returnRows.forEach(row => {
                                    frappe.model.set_value(row.doctype, row.name, 'return_processed', 1);
                                });
                            }
                            resolve();
                        }
                    });
                });
            }
        }
    },

    interest_rate: function (frm) {
        if (frm.doc.table_zjnd && frm.doc.interest_rate && frm.doc.table_zjnd.length > 0) {
            frm.doc.table_zjnd.forEach((item) => {
                item.interest_rate = frm.doc.interest_rate || 0;
            });
            frm.refresh_field("table_zjnd");
        }
    },

    end_date: function (frm) {
        if (frm.doc.table_zjnd && frm.doc.table_zjnd.length > 0) {
            frm.doc.table_zjnd.forEach((item) => {
                item.return_date = frm.doc.end_date || 0;
            });
            frm.refresh_field("table_zjnd");
        }
    },  
});
