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
    }
})