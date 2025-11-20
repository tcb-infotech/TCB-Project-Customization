frappe.ui.form.on("Compensation Records",{
    validate:function(frm,cdt,cdn){
        calculate_total(frm,cdt,cdn)
    }

})

function calculate_total(frm,cdt,cdn){
    let sum = 0
    frm.doc.compensation_areas.forEach((row)=>{
        sum+= (row.land+row.rasta+row.foundation+row.stringing+row.crop+row.compensation_enabling+row.erection+row.utr_no)
    })
    frm.set_value("paid_total_amount",sum)
}