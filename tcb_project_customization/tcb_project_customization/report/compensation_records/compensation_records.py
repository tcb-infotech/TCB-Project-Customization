# Copyright (c) 2025, AjayRaj Mahiwal and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
    filters = filters or {}
    columns=[
        {"fieldname":"project","label":"Project","fieldtype":"Link","options":"Project","width":170},
        {"fieldname":"tower_no","label":"Tower No","fieldtype":"Data","width":170},
        {"fieldname":"posting_date","label":"Posting Date","fieldtype":"Date","width":170},
        {"fieldname":"farmer_name","label":"Farmer Name","fieldtype":"Data","width":170},
        {"fieldname":"address","label":"Address","fieldtype":"Data","width":170},
        {"fieldname":"ac_no","label":"A/C No","fieldtype":"Data","width":170},
        {"fieldname":"ifsc_code","label":"IFSC Code","fieldtype":"Data","width":170},
        {"fieldname":"micro_code","label":"Micro Code","fieldtype":"Data","width":170},
        {"fieldname":"bank_name","label":"Bank Name","fieldtype":"Data","width":170},
        {"fieldname":"land","label":"Land","fieldtype":"Float","width":170},
        {"fieldname":"crop","label":"Crop","fieldtype":"Float","width":170},
        {"fieldname":"rasta","label":"Rasta","fieldtype":"Float","width":170},
        {"fieldname":"stringing","label":"Stringing","fieldtype":"Float","width":170},
        {"fieldname":"paid_total_amt","label":"Paid Total Amt","fieldtype":"Float","width":170},
        {"fieldname":"payment_date","label":"Payment Date","fieldtype":"Date","width":170},
        {"fieldname":"utr_id","label":"UTR ID","fieldtype":"Data","width":170},
        {"fieldname":"last_payment","label":"Last Payment","fieldtype":"Data","width":170},
        {"fieldname":"grand_total","label":"Grand Total","fieldtype":"Float","width":170}
    ]
    data=[]
    
    c_records = frappe.db.get_all("Compensation Records",
                                  filters={"docstatus":1},
                                  fields=["*"])
    
    for records in c_records:
        data.append({
            "project":records.project,
            "tower_no":records.tower_no,
            "posting_date":records.posting_date,
            "farmer_name":records.name_of_farmer,
            "address":records.address,
            "ac_no":records.ac_no,
            "ifsc_code":records.ifsc_code,
            "micro_code":records.micro_code,
            "bank_name":records.bank_name,
            "land":records.land,
            "crop":records.crop,
            "rasta":records.rasta,
            "stringing":records.stringing,
            "paid_total_amt":records.paid_total_amount,
            "payment_date":records.payment_date,
            "utr_id":records.utr_id,
            "last_payment":records.last_payment_remarks,
            "grand_total":records.grand_total
        })
    
    return columns, data
