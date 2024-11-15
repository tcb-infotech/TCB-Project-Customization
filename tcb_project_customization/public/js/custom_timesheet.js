frappe.ui.form.on("Timesheet",{
    refresh(frm){
        frm.set_df_property("time_logs","reqd",0);
    }
})