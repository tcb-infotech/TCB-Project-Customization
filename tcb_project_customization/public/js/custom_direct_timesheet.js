frappe.ui.form.on("Direct Timesheet",{
    refresh:function(frm){
        if(frm.doc.docstatus==1){
            frm.add_custom_button("DPR Detail",()=>{
                frappe.new_doc("DPR Detail")
            })
        }
    }
})