# Copyright (c) 2024, AjayRaj Mahiwal and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt

from erpnext.accounts.report.financial_statements import get_period_list


def execute(filters=None):
	filters = frappe._dict(filters or {})

	columns = get_columns()
	data = get_vehicle_log_data(filters)
	chart = get_chart_data(data, filters)

	return columns, data, None, chart


def get_columns():
	return [
		{
			"fieldname": "log_name",
			"fieldtype": "Link",
			"label": _("Vehicle Log"),
			"options": "Vehicle Log",
			"width": 150,
		},
		{
			"fieldname": "vehicle",
			"fieldtype": "Link",
			"label": _("Vehicle Plate"),
			"options": "Vehicle",
			"width": 150,
		},
		{"fieldname": "custom_vehicle_type", "fieldtype": "Data", "label": _("Vehicle Type"), "width": 120},
		{"fieldname": "model", "fieldtype": "Data", "label": _("Model"), "width": 120},
		{"fieldname": "location", "fieldtype": "Link","options":"Location", "label": _("Location"), "width": 130},
		# {"fieldname": "project", "fieldtype": "Link","options":"Project", "label": _("Project"), "width": 100},
		# {"fieldname": "project_name", "fieldtype": "Data", "label": _("Project Name"), "width": 150},
		{"fieldname": "odometer", "fieldtype": "Int", "label": _("Odometer Value"), "width": 120},
		{"fieldname": "date", "fieldtype": "Date", "label": _("Date"), "width": 100},
		{"fieldname": "fuel_qty", "fieldtype": "Float", "label": _("Fuel Qty"), "width": 80},
		{"fieldname": "fuel_price", "fieldtype": "Float", "label": _("Fuel Price"), "width": 100},
		{"fieldname": "fuel_expense", "fieldtype": "Currency", "label": _("Fuel Expense"), "width": 150},
		{
			"fieldname": "service_expense",
			"fieldtype": "Currency",
			"label": _("Service Expense"),
			"width": 150,
		},
		{
			"fieldname": "employee",
			"fieldtype": "Link",
			"label": _("Employee"),
			"options": "Employee",
			"width": 150,
		},
		{
			"fieldname": "employee_name",
			"fieldtype": "Data",
			"label": _("Employee Name"),
			"width": 150,
		},
	]


def get_vehicle_log_data(filters):
	conditions, values = get_conditions(filters)

	# nosemgrep: frappe-semgrep-rules.rules.frappe-using-db-sql
	data = frappe.db.sql(
		f"""
			SELECT 
				vhcl.license_plate as vehicle,
				vhcl.custom_vehicle_type,
				vhcl.model,
				log.name as log_name,
				log.odometer,
				log.date,
				log.employee,
				emp.employee_name,
				log.fuel_qty,
				log.custom_current_location as location,
				log.price as fuel_price,
				log.fuel_qty * log.price as fuel_expense
			FROM `tabVehicle` vhcl
			INNER JOIN `tabVehicle Log` log ON vhcl.license_plate = log.license_plate
			LEFT JOIN `tabEmployee` emp ON log.employee = emp.name
			WHERE log.docstatus = 1 
			{conditions}
			ORDER BY date""",
			values,
			as_dict=1,
	)

	for row in data:
		row["service_expense"] = get_service_expense(row.log_name)

	return data


def get_conditions(filters):
	conditions = ""

	start_date, end_date = get_period_dates(filters)

	if start_date and end_date:
		conditions += "AND date between %(start_date)s and %(end_date)s"
		values = {"start_date": start_date, "end_date": end_date}

		if filters.employee:
			conditions += " and log.employee = %(employee)s"
			values["employee"] = filters.employee

		if filters.vehicle:
			conditions += " and vhcl.license_plate = %(vehicle)s"
			values["vehicle"] = filters.vehicle

		if filters.location:
			conditions += " and log.custom_current_location = %(location)s"
			values["location"] = filters.location
		
		if filters.get("custom_vehicle_type"):
			conditions += "AND vhcl.custom_vehicle_type = %(custom_vehicle_type)s"
			values["custom_vehicle_type"] = filters.custom_vehicle_type
			
		if filters.get("model"):
			conditions += "AND vhcl.model Like %(model)s"
			values["model"] = filters.model


	# if filters.project:
	# 	conditions += " and log.custom_current_project = %(project)s"
	# 	values["project"] = filters.project

	return conditions, values


def get_period_dates(filters):
	if filters.filter_based_on == "Fiscal Year" and filters.fiscal_year:
		fy = frappe.db.get_value(
			"Fiscal Year", filters.fiscal_year, ["year_start_date", "year_end_date"], as_dict=True
		)
		return fy.year_start_date, fy.year_end_date
	else:
		return filters.from_date, filters.to_date


def get_service_expense(logname):
	expense_amount = frappe.db.sql(
		"""
		SELECT sum(expense)
		FROM
			`tabVehicle Log` log, `tabVehicle Service HRC` service
		WHERE
			service.parent=log.name and log.name=%s
	""",
		logname,
	)

	return flt(expense_amount[0][0]) if expense_amount else 0.0


def get_chart_data(data, filters):
	period_list = get_period_list(
		filters.fiscal_year,
		filters.fiscal_year,
		filters.from_date,
		filters.to_date,
		filters.filter_based_on,
		"Monthly",
	)

	fuel_data, service_data = [], []

	for period in period_list:
		total_fuel_exp = 0
		total_service_exp = 0

		for row in data:
			if row.date <= period.to_date and row.date >= period.from_date:
				total_fuel_exp += flt(row.fuel_expense)
				total_service_exp += flt(row.service_expense)

		fuel_data.append([period.key, total_fuel_exp])
		service_data.append([period.key, total_service_exp])

	labels = [period.label for period in period_list]
	fuel_exp_data = [row[1] for row in fuel_data]
	service_exp_data = [row[1] for row in service_data]

	datasets = []
	if fuel_exp_data:
		datasets.append({"name": _("Fuel Expenses"), "values": fuel_exp_data})

	if service_exp_data:
		datasets.append({"name": _("Service Expenses"), "values": service_exp_data})

	chart = {
		"data": {"labels": labels, "datasets": datasets},
		"type": "line",
		"fieldtype": "Currency",
	}

	return chart
