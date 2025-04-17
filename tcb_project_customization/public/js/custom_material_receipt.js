frappe.ui.form.on("Stock Entry",{
    stock_entry_type:function(frm){
        if (frm.is_new()) {
            if(frm.doc.stock_entry_type=="Material Transfer"){
                frm.set_value("naming_series","HRC-")
            }
            frm.refresh_field("naming_series");
    }  }
})