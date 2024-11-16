frappe.ui.form.on('Purchase Order', {
    custom_required_by: function(frm) {
        if (frm.doc.custom_required_by) {
            let today = new Date();

            let days_to_add = frm.doc.custom_required_by;

            let newDate = new Date(today.setDate(today.getDate() + days_to_add));

            frm.set_value('schedule_date', newDate);

            frm.set_df_property('schedule_date','read_only',1)
            frm.refresh_field('schedule_date');
        }
        else{
            // becomes editable if no days entered
            frm.set_df_property('schedule_date','read_only',0)
            frm.refresh_field('schedule_date')
        }
    },
    onload: function(frm) {
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
});


