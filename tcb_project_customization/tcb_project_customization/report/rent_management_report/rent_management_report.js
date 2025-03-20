
frappe.query_reports["Rent Management Report"] = {
    "filters": [
        {
            "fieldname": "customer",
            "label": "Customer",
            "fieldtype": "Link",
            "options": "Customer"
        },
        {
            "fieldname": "start_date",
            "label": "Date From",
            "fieldtype": "Date",
        },
        {
            "fieldname": "end_date",
            "label": "Date To",
            "fieldtype": "Date",
        },
        {
            "fieldname": "warehouse",
            "label": "Warehouse",
            "fieldtype": "Link",
            "options": "Warehouse"
        },
        {
            "fieldname": "rent_item",
            "label": "Rent Item",
            "fieldtype": "Link",
            "options": "Item"
        },
        {
            "fieldname": "status",
            "label": "Status",
            "fieldtype": "Select",
            "options": "\nOngoing\nCompleted\nOverdue"
        },
        {
            "fieldname": "min_amount",
            "label": "Minimum Amount",
            "fieldtype": "Float"
        },
        {
            "fieldname": "max_amount",
            "label": "Maximum Amount",
            "fieldtype": "Float"
        }
    ]
};