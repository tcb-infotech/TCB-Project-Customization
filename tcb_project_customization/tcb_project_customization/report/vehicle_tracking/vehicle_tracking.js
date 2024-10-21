// Copyright (c) 2024, AjayRaj Mahiwal and contributors
// For license information, please see license.txt

frappe.query_reports["Vehicle Tracking"] = {
    "filters": [
        {
            "fieldname": "custom_project",
            "label": __("Project"),
            "fieldtype": "Link",
            "options": "Project"
        },
        {
            "fieldname": "custom_project_name",
            "label": __("Project Name"),
            "fieldtype": "Data"
        },
        {
            "fieldname": "make",
            "label": __("Make"),
            "fieldtype": "Data"
        },
        {
            "fieldname": "status",
            "label": __("Status"),
            "fieldtype": "Select",
            "options": "\nIn Service\nOut of Service\nMaintenance"
        }
    ]
};