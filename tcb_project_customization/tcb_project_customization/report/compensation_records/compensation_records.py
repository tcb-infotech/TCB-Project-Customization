# Copyright (c) 2025, AjayRaj Mahiwal and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    filters = filters or {}

    columns = [
        {"fieldname":"id","label":"ID","fieldtype":"Link","options":"Compensation Records","width":170},
        {"fieldname":"project","label":"Project","fieldtype":"Link","options":"Project","width":170},
        {"fieldname":"tower_no","label":"Tower No","fieldtype":"Data","width":170},
        {"fieldname":"posting_date","label":"Posting Date","fieldtype":"Date","width":170},
        {"fieldname":"farmer_name","label":"Farmer Name","fieldtype":"Data","width":170},
        {"fieldname":"address","label":"Address","fieldtype":"Data","width":170},
        {"fieldname":"ac_no","label":"A/C No","fieldtype":"Data","width":170},
        {"fieldname":"ifsc_code","label":"IFSC Code","fieldtype":"Data","width":170},
        {"fieldname":"micro_code","label":"Micro Code","fieldtype":"Data","width":170},
        {"fieldname":"bank_name","label":"Bank Name","fieldtype":"Data","width":170},
        {"fieldname":"total_compensated_amount","label":"Total Compensated Amount","fieldtype":"Currency","width":170},
        
        {"fieldname":"payment_date","label":"Payment Date","fieldtype":"Date","width":170},
        {"fieldname":"land","label":"Land","fieldtype":"Currency","width":170},
        {"fieldname":"crop","label":"Crop","fieldtype":"Currency","width":170},
        {"fieldname":"rasta","label":"Rasta","fieldtype":"Currency","width":170},
        {"fieldname":"stringing","label":"Stringing","fieldtype":"Currency","width":170},
        {"fieldname":"foundation","label":"Foundation","fieldtype":"Currency","width":170},
        {"fieldname":"erection","label":"Erection","fieldtype":"Currency","width":170},
        {"fieldname":"compensation_enabling","label":"Compensation Enabling","fieldtype":"Currency","width":220},
        {"fieldname":"rems","label":"Remarks","fieldtype":"Small Text","width":170},
        {"fieldname":"paid_total_amt","label":"Paid Total Amt","fieldtype":"Currency","width":170},
        {"fieldname":"utr_id","label":"UTR ID","fieldtype":"Data","width":170},
        {"fieldname":"farmer_name_filter","label":"Farmer Name(For Filter)","fieldtype":"Data","width":170},
        {"fieldname":"remarks","label":"Record Remarks","fieldtype":"Data","width":170},
    ]

    data = []

    table_records = frappe.db.get_all(
        "Compensation Areas",
        fields=["*"],
        order_by="parent, idx"
    )

    last_parent = None

    for record in table_records:
        parent = frappe.get_doc("Compensation Records", record.parent)

        row = {
            "id": parent.name,
            "project": parent.project,
            "tower_no": parent.tower_no,
            "posting_date": parent.posting_date,
            "farmer_name": parent.name_of_farmer,
            "address": parent.address,
            "ac_no": parent.ac_no,
            "ifsc_code": parent.ifsc_code,
            "micro_code": parent.micro_code,
            "bank_name": parent.bank_name,

            "payment_date": record.compensation_date,
            "land": record.land,
            "crop": record.crop,
            "rasta": record.rasta,
            "stringing": record.stringing,
            "foundation": record.foundation,
            "erection": record.erection,
            "compensation_enabling": record.compensation_enabling,
            "rems": record.remarks,
            "paid_total_amt": parent.paid_total_amount,
            "utr_id": record.utr_no,
            "remarks": parent.remarks,
            "farmer_name_filter":parent.name_of_farmer,
            "total_compensated_amount":parent.paid_total_amount
        }

        if record.parent == last_parent:
            row.update({
                "id": "",
                "project": "",
                "tower_no": "",
                "posting_date": "",
                "farmer_name": "",
                "address": "",
                "ac_no": "",
                "ifsc_code": "",
                "micro_code": "",
                "bank_name": "",
                "paid_total_amt": "",
                "remarks": "",
                "total_compensated_amount":""
            })
        else:
            last_parent = record.parent

        data.append(row)

    return columns, data
