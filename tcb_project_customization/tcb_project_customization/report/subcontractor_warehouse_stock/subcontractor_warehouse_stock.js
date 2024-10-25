// Copyright (c) 2024, AjayRaj Mahiwal and contributors
// For license information, please see license.txt

frappe.query_reports["Subcontractor Warehouse Stock"] = {
    filters: [
        {
            fieldname: "company",
            label: __("Company"),
            fieldtype: "Link",
            options: "Company",
            default: frappe.defaults.get_user_default("Company"),
            reqd: 1
        },
        {
            fieldname: "from_date",
            label: __("From Date"),
            fieldtype: "Date",
            default: frappe.datetime.add_months(frappe.datetime.get_today(), -6),
        },
        {
            fieldname: "to_date",
            label: __("To Date"),
            fieldtype: "Date",
            default: frappe.datetime.get_today(),
        },
        {
            fieldname: "subcontractor",
            label: __("Subcontractor"),
            fieldtype: "Link",
            options: "Subcontractor"
        },
        {
            fieldname: "warehouse",
            label: __("Warehouse"),
            fieldtype: "Link",
            options: "Warehouse",
            get_query: function() {
                return {
                    filters: {
                        'custom_subcontractor': ['!=', '']
                    }
                };
            }
        },
        {
            fieldname: "project",
            label: __("Project"),
            fieldtype: "Link",
            options: "Project"
        }
    ],

    formatter: function(value, row, column, data, default_formatter) {
        value = default_formatter(value, row, column, data);

        if (column.fieldname == "stock_value" && data && data.stock_value < 0) {
            value = "<span style='color:red'>" + value + "</span>";
        }

        return value;
    },

    get_chart_data: function(columns, result) {
        return {
            data: {
                labels: result.map(d => d.warehouse || ''),
                datasets: [{
                    name: "Stock Value",
                    values: result.map(d => d.stock_value || 0)
                }]
            },
            type: 'bar',
            height: 280
        };
    }
};