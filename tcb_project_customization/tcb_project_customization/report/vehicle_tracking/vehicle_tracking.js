// Copyright (c) 2024, AjayRaj Mahiwal and contributors
// For license information, please see license.txt

frappe.query_reports["Vehicle Tracking"] = {
    "filters": [
        // {
        //     "fieldname": "custom_project",
        //     "label": __("Project"),
        //     "fieldtype": "Link",
        //     "options": "Project"
        // },
        // {
        //     "fieldname": "custom_project",
        //     "label": __("Project"),
        //     "fieldtype": "Link",
        //     "options": "Project"
        // },
        {
            "fieldname": "custom_vehicle_location",
            "label": __("Location"),
            "fieldtype": "Link",
            "options": "Location"
        },
        {
            "fieldname": "model",
            "label": __("Model"),
            "fieldtype": "Data",
        },
        // {
        //     "fieldname": "custom_project_name",
        //     "label": __("Project Name"),
        //     "fieldtype": "Data"
        // },
        {
            "fieldname": "make",
            "label": __("Make"),
            "fieldtype": "Data"
        },
        // {
        //     "fieldname": "status",
        //     "label": __("Status"),
        //     "fieldtype": "Select",
        //     "options": "\nIn Service\nOut of Service\nMaintenance"
        // }
    ],
    onload: function(report) {
        setTimeout(() => {
            // Get the datatable instance
            if (report.datatable && report.datatable.rowmanager) {
                // Collapse all rows
                report.datatable.rowmanager.collapseAllNodes();
                
                // Show expand all button and hide collapse all button
                report.$report.find('[data-action="expand_all_rows"]').show();
                report.$report.find('[data-action="collapse_all_rows"]').hide();
            }
        }, 300);
    },

};

