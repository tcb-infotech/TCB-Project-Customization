frappe.ui.form.on("Inspection",{
    onload: function(frm) {
        if(!frm.doc.custom_financial_year){
            const today = new Date();
            let startYear, endYear;
    
            if (today.getMonth() >= 3) { 
                startYear = today.getFullYear();
                endYear = startYear + 1;
            } else { 
                endYear = today.getFullYear();
                startYear = endYear - 1;
            }
    
            const financialYear = `${startYear.toString().slice(-2)}-${endYear.toString().slice(-2)}`;
            frm.set_value('custom_financial_year', financialYear);
            
        }
    },
    on_submit:function(frm){
        if(frm.doc.custom_sales_order){
            link_so_inspection(frm)
        }
    }
})


function link_so_inspection(frm){
    if(frm.doc.custom_sales_order && frm.doc.docstatus == 1){
        frappe.call({
            method:"frappe.client.get",
            args:{
                doctype:"Sales Order",
                name:frm.doc.custom_sales_order,
                fieldname:["custom_boq_inspections"],
            },
            callback:(r)=>{
                if(r.message){
                    let existing = r.message.custom_boq_inspections || ""
                    let inspections = existing ? existing.split(", ") : []

                    if (!inspections.includes(frm.doc.name)) {
                        inspections.push(frm.doc.name);

                        frappe.call({
                            method: "frappe.client.set_value",
                            args: {
                                doctype: "Sales Order",
                                name: frm.doc.custom_sales_order,
                                fieldname: "custom_boq_inspections",
                                value: inspections.join(", "),
                            },
                            callback: function (res) {
                                if (!res.exc) {
                                    frappe.msgprint("Linked successfully to Sales Order!");
                                }
                            },
                        });


                    }
                    
                }
            }
        })
    }
}

