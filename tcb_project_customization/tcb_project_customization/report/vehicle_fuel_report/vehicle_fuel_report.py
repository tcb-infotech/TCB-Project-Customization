# Copyright (c) 2026, AjayRaj Mahiwal and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
	columns = [
		{
			"label": "Log ID",
			"fieldname": "log_id",
			"fieldtype": "Link",
			"options": "Vehicle Log",
			"width": 200
		},
		{
			"label": "Date",
			"fieldname": "date",
			"fieldtype": "Date",
			"width": 120
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
			"label": "Odometer (KM)",
			"fieldname": "odometer",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label": "Fuel Qty",
			"fieldname": "fuel_qty",
			"fieldtype": "Float",
			"width": 100
		},
		{
			"label": "Fuel Price (Per Litre)",
			"fieldname": "fuel_price",
			"fieldtype": "Currency",
			"width": 140
		},
		{
			"label": "Total Amount",
			"fieldname": "total_amount",
			"fieldtype": "Currency",
			"width": 140
		}
	]

	data = frappe.db.sql("""
		SELECT
			vl.name AS log_id,
			vl.date,
			vl.license_plate,
			vl.model,
			vl.odometer,
			vl.fuel_qty,
			vl.price AS fuel_price,
			(vl.fuel_qty * vl.price) AS total_amount
		FROM `tabVehicle Log` vl
		INNER JOIN (
			SELECT
				license_plate,
				MAX(date) AS latest_date
			FROM `tabVehicle Log`
			WHERE
				docstatus = 1
				AND fuel_qty IS NOT NULL
				AND fuel_qty > 0
			GROUP BY license_plate
		) latest
			ON latest.license_plate = vl.license_plate
		AND latest.latest_date = vl.date
		WHERE
			vl.docstatus = 1
			AND vl.fuel_qty IS NOT NULL
			AND vl.fuel_qty > 0
		ORDER BY vl.license_plate
	""", as_dict=True)

	return columns, data
