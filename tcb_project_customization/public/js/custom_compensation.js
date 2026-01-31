frappe.ui.form.on("Compensation Records",{
    validate:function(frm,cdt,cdn){
        calculate_total(frm,cdt,cdn)
    }

})

function calculate_total(frm,cdt,cdn){
    let sum = 0
    frm.doc.compensation_areas.forEach((row)=>{
        sum +=
            (row.land || 0) +
            (row.rasta || 0) +
            (row.foundation || 0) +
            (row.stringing || 0) +
            (row.crop || 0) +
            (row.compensation_enabling || 0) +
            (row.erection || 0)
    })
    frm.set_value("paid_total_amount",sum)
}