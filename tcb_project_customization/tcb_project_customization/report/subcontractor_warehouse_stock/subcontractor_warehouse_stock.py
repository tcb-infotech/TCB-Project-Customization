
from frappe import _
import frappe
from frappe.utils import flt

def execute(filters=None):
    if not filters:
        filters = {}

    columns = get_columns()
    data = get_stock_balance_data(filters)
    
    return columns, data

def get_columns():
    return [
        {
            "fieldname": "subcontractor",
            "label": _("Subcontractor"),
            "fieldtype": "Link",
            "options": "Subcontractor",
            "width": 200
        },
        {
            "fieldname": "subcontractor_name",
            "label": _("Subcontractor Name"),
            "fieldtype": "Data",
            "width": 200
        },
        {
            "fieldname": "warehouse",
            "label": _("Warehouse"),
            "fieldtype": "Link",
            "options": "Warehouse",
            "width": 180
        },
        {
            "fieldname": "project",
            "label": _("Project"),
            "fieldtype": "Link",
            "options": "Project",
            "width": 140
        },
        {
            "fieldname": "project_name",
            "label": _("Project Name"),
            "fieldtype": "Data",
            "width": 140
        },
        {
            "fieldname": "stock_value",
            "label": _("Stock Value"),
            "fieldtype": "Currency",
            "width": 140
        },
        {
            "fieldname": "qty",
            "label": _("Quantity"),
            "fieldtype": "Float",
            "width": 120
        }
    ]

def get_stock_balance_data(filters):
    conditions = get_conditions(filters)
    
    warehouse_query = """
        SELECT 
            w.name as warehouse,
            w.custom_subcontractor as subcontractor,
            w.custom_project as project,
            s.subcontractor_name,
            p.project_name
        FROM `tabWarehouse` w
        LEFT JOIN `tabSubcontractor` s ON w.custom_subcontractor = s.name
        LEFT JOIN `tabProject` p ON w.custom_project = p.name
        WHERE w.custom_subcontractor IS NOT NULL
        AND w.custom_subcontractor != ''
        {conditions}
        ORDER BY w.name
    """.format(conditions=conditions)

    data = frappe.db.sql(warehouse_query, filters, as_dict=1)

    # Get stock balances for each warehouse
    for row in data:
        balance_data = get_balance_qty_and_value(row.warehouse, filters)
        row.update(balance_data)

    return data

def get_conditions(filters):
    conditions = []
    
    if filters.get("company"):
        conditions.append("w.company = %(company)s")
    
    if filters.get("subcontractor"):
        conditions.append("w.custom_subcontractor = %(subcontractor)s")
    
    if filters.get("warehouse"):
        conditions.append("w.name = %(warehouse)s")
        
    if filters.get("project"):
        conditions.append("w.custom_project = %(project)s")

    return " AND " + " AND ".join(conditions) if conditions else ""

def get_balance_qty_and_value(warehouse, filters):
    query_filters = {"warehouse": warehouse}
    query_conditions = ["warehouse = %(warehouse)s", "is_cancelled = 0"]
    
    if filters.get("from_date"):
        query_filters["from_date"] = filters.get("from_date")
        query_conditions.append("posting_date >= %(from_date)s")
    
    if filters.get("to_date"):
        query_filters["to_date"] = filters.get("to_date")
        query_conditions.append("posting_date <= %(to_date)s")
    
    conditions = " AND ".join(query_conditions)
    
    result = frappe.db.sql("""
        SELECT 
            SUM(actual_qty) as qty,
            SUM(stock_value_difference) as stock_value
        FROM `tabStock Ledger Entry`
        WHERE {conditions}
    """.format(conditions=conditions), 
    query_filters,
    as_dict=1)
    
    return result[0] if result else {"qty": 0, "stock_value": 0}