frappe.ui.form.on("Inspection",{
    refresh:function(frm){
        frm.fields_dict["inspector"].get_query =  function(doc,cdt,cdn){
            return{
                filters:{
                    custom_inspection_inspector:1
                }
            }
        }
    }
})