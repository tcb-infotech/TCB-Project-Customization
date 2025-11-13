# Copyright (c) 2025, AjayRaj Mahiwal and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
    filters = filters or {}
    columns=[
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
        {"fieldname":"land","label":"Land","fieldtype":"Float","width":170},
        {"fieldname":"crop","label":"Crop","fieldtype":"Float","width":170},
        {"fieldname":"rasta","label":"Rasta","fieldtype":"Float","width":170},
        {"fieldname":"stringing","label":"Stringing","fieldtype":"Float","width":170},
        {"fieldname":"foundation","label":"Foundation","fieldtype":"Float","width":170},
        {"fieldname":"compensation_enabling","label":"Compensation Enabling","fieldtype":"Float","width":220},
        {"fieldname":"paid_total_amt","label":"Paid Total Amt","fieldtype":"Float","width":170},
        {"fieldname":"payment_date","label":"Payment Date","fieldtype":"Date","width":170},
        {"fieldname":"utr_id","label":"UTR ID","fieldtype":"Data","width":170},
        {"fieldname":"last_payment","label":"Last Payment Remarks","fieldtype":"Data","width":170},
        {"fieldname":"grand_total","label":"Grand Total","fieldtype":"Float","width":170}
    ]
    data=[]
    
    
    table_records = frappe.db.get_all("Compensation Areas",
                                      filters={"modified":["between",[filters.get("from_date"),filters.get("to_date")]]},
                                      fields =["*"])
    
    # rows ={}
    for record in table_records:
        
        parent = frappe.get_doc("Compensation Records",record.parent)
        
        # key = f"{parent.name}-{record.name}"
        # if key not in rows:
        #     rows.setdefault(key,[])
        
        rows={
            "id":parent.name,
            "project":parent.project,
            "tower_no":parent.tower_no,
            "posting_date":parent.posting_date,
            "farmer_name":parent.name_of_farmer,
            "address":parent.address,
            "ac_no":parent.ac_no,
            "ifsc_code":parent.ifsc_code,
            "micro_code":parent.micro_code,
            "bank_name":parent.bank_name,
            "land":record.land,
            "crop":record.crop,
            "rasta":record.rasta,
            "stringing":record.stringing,
            "foundation":record.foundation,
            "compensation_enabling":record.compensation_enabling,
            "paid_total_amt":parent.paid_total_amount,
            "payment_date":parent.payment_date,
            "utr_id":parent.utr_id,
            "last_payment":parent.last_payment_remarks,
            "grand_total":parent.grand_total
        }
        
    data.append(rows)
    
    return columns, data
