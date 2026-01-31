# Copyright (c) 2026, AjayRaj Mahiwal and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    filters = filters or {}

    columns = [
        {
            "label": "Log Id",
            "fieldname": "log_id",
            "fieldtype": "Link",
            "options": "Vehicle Log",
            "width": 200
        },
        {
            "label": "Date",
            "fieldname": "date",
            "fieldtype": "Date",
            "width": 140
        },
        {
            "label": "License Plate",
            "fieldname": "license_plate",
            "fieldtype": "Link",
            "options": "Vehicle",
            "width": 140
        },
        {
            "label": "Model",
            "fieldname": "model",
            "fieldtype": "Data",
            "width": 180
        },
        {
            "label": "Odometer(KM)",
            "fieldname": "odometer",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": "Service Item",
            "fieldname": "service_item",
            "fieldtype": "Data",
            "width": 180
        },
        {
            "label": "Operation",
            "fieldname": "type",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": "Expense",
            "fieldname": "expense_amount",
            "fieldtype": "Currency",
            "width": 100
        },
        {
            "label": "Remarks",
            "fieldname": "custom_remarks",
            "fieldtype": "Data",
            "width": 250
        }
    ]

    conditions = []
    values = {}

    if filters.get("vehicle"):
        conditions.append("vl.license_plate = %(vehicle)s")
        values["vehicle"] = filters["vehicle"]

    if filters.get("from_date"):
        conditions.append("vl.date >= %(from_date)s")
        values["from_date"] = filters["from_date"]

    if filters.get("to_date"):
        conditions.append("vl.date <= %(to_date)s")
        values["to_date"] = filters["to_date"]

    condition_sql = ""
    if conditions:
        condition_sql = " AND " + " AND ".join(conditions)

    raw_data = frappe.db.sql(f"""
            SELECT
                vl.name AS log_id,
                vl.license_plate,
                vl.model,
                vl.date,
                vl.odometer,
                vs.service_item,
                vs.type,
                vs.custom_remarks,
                vs.expense_amount
            FROM `tabVehicle Log` vl
            INNER JOIN `tabVehicle Service` vs
                ON vs.parent = vl.name
            WHERE
                vl.docstatus = 1
                {condition_sql}
            ORDER BY
                vl.license_plate,
                vl.date,
                vl.name,
                vs.idx
        """, values, as_dict=True)

    data = []
    last_log = None

    for row in raw_data:
        if row["log_id"] == last_log:
            row["license_plate"] = ""
            row["model"] = ""
            row["log_id"] = ""
            row["date"] = ""
            row["odometer"] = ""
        else:
            last_log = row["log_id"]

        data.append(row)


    return columns, data
