// Copyright (c) 2025, AjayRaj Mahiwal and contributors
// For license information, please see license.txt

frappe.query_reports["Compensation Records"] = {
	"filters": [
		{
			fieldname:"from_date",
			label:"From Date",
			fieldtype:"Date",
			default:frappe.datetime.now_date()
		},
		{
			fieldname:"to_date",
			label:"To Date",
			fieldtype:"Date",
			default:frappe.datetime.now_date()
		}
	]
};
