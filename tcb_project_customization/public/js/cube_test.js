frappe.ui.form.on("Cube Test",{
    onload:function(frm){
        frm.get_field("supplier_address").get_query = ((doc)=>{
            return{
                filters:{
                    link_doctype : "Supplier",
                    link_name : doc.supplier
                }
            }
        })
    }
})