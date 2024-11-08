frappe.ui.form.on("Warehouse", {
    refresh: function(frm){
        frm.set_query("custom_subcontractor", function(){
            return{
                "filters": {
                    "designation": "Gang Leader"
                }
            }
        });
    }
});