# Copyright (c) 2026, AjayRaj Mahiwal and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import add_months, today

def execute(filters=None):
    filters = filters or {}

    # default last 1 month
    if not filters.get("from_date"):
        filters["from_date"] = add_months(today(), -1)

    if not filters.get("to_date"):
        filters["to_date"] = today()

    conditions = []
    values = filters

    if filters.get("from_date"):
        conditions.append("vl.date >= %(from_date)s")

    if filters.get("to_date"):
        conditions.append("vl.date <= %(to_date)s")

    if filters.get("vehicle"):
        conditions.append("vl.license_plate = %(vehicle)s")

    condition_sql = " AND ".join(conditions)

    columns = [
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
            "width": 200
        },
        # {
        #     "label": "KM Run",
        #     "fieldname": "km_run",
        #     "fieldtype": "Float",
        #     "width": 120
        # },
        {
            "label": "Current Mileage",
            "fieldname": "current_mileage",
            "fieldtype": "Float",
            "width": 140
        },
        {
            "label": "Total Fuel Qty",
            "fieldname": "total_fuel_qty",
            "fieldtype": "Float",
            "width": 140
        },
        {
            "label": "Total Fuel Amount",
            "fieldname": "total_amount",
            "fieldtype": "Currency",
            "width": 160
        }
    ]

    data = frappe.db.sql(f"""
        SELECT
            vl.license_plate,
            MAX(vl.model) AS model,
            v.custom_vehicle_mileage as current_mileage,
            # (MAX(vl.odometer) - MIN(vl.odometer)) AS km_run,
            SUM(vl.fuel_qty) AS total_fuel_qty,
            SUM(vl.fuel_qty * vl.price) AS total_amount
        FROM `tabVehicle Log` vl
        join `tabVehicle` v on vl.license_plate = v.name
        WHERE
            vl.docstatus = 1
            AND vl.fuel_qty IS NOT NULL
            AND vl.fuel_qty > 0
            AND {condition_sql}
        GROUP BY vl.license_plate
        ORDER BY vl.license_plate
    """, values, as_dict=True)

    return columns, data
