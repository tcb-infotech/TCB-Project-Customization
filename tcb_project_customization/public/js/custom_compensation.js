frappe.ui.form.on("Compensation Records",{
    land:function(frm){
        calculate_total(frm)
    },
    crop:function(frm){
        calculate_total(frm)
    },
    rasta:function(frm){
        calculate_total(frm)
    },
    stringing:function(frm){
        calculate_total(frm)
    },
})

function calculate_total(frm){
    frm.set_value("paid_total_amount",flt(frm.doc.land+frm.doc.rasta+frm.doc.crop+frm.doc.stringing))
}