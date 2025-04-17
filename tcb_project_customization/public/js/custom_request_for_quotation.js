frappe.ui.form.on("Request for Quotation",{
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
        }
        
})