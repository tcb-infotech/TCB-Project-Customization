// Copyright (c) 2026, AjayRaj Mahiwal and contributors
// For license information, please see license.txt

frappe.query_reports["Vehicle Service Report"] = {
	filters: [
		{
			fieldname: "vehicle",
			label: "Vehicle",
			fieldtype: "Link",
			options: "Vehicle"
		},
		{
			fieldname: "from_date",
			label: "From Date",
			fieldtype: "Date",
			default: frappe.datetime.add_months(frappe.datetime.get_today(), -1)
		},
		{
			fieldname: "to_date",
			label: "To Date",
			fieldtype: "Date",
			default: frappe.datetime.get_today()
		}
	]
};
