import frappe
from frappe.utils import flt

def execute(filters=None):
    filters = filters or {}
    conditions = ""

    if filters.get("po"):
        conditions += f" AND po.name = {frappe.db.escape(filters['po'])}"

    if filters.get("item_code"):
        conditions += f" AND poi.item_code = {frappe.db.escape(filters['item_code'])}"

    if filters.get("from_date"):
        conditions += f" AND pr.posting_date >= {frappe.db.escape(filters['from_date'])}"

    if filters.get("to_date"):
        conditions += f" AND pr.posting_date <= {frappe.db.escape(filters['to_date'])}"

    data = frappe.db.sql(f"""
        SELECT
            po.name AS purchase_order,
            pr.name AS purchase_receipt,
            poi.item_code,
            poi.qty AS ordered_qty,
            IFNULL(SUM(pri.qty), 0) AS received_qty,
            CASE
                WHEN IFNULL(SUM(pri.qty), 0) >= poi.qty THEN 'Completed'
                ELSE 'Pending'
            END AS status
        FROM
            `tabPurchase Order` po
        JOIN
            `tabPurchase Order Item` poi ON poi.parent = po.name
        LEFT JOIN
            `tabPurchase Receipt Item` pri ON pri.purchase_order_item = poi.name
        LEFT JOIN
            `tabPurchase Receipt` pr ON pri.parent = pr.name AND pr.docstatus = 1
        WHERE
            po.docstatus = 1
            {conditions}
        GROUP BY
            po.name, pr.name, poi.item_code, poi.qty
    """, as_dict=1)

    # Apply status filter manually (since it's a calculated field)
    if filters.get("status"):
        data = [d for d in data if d["status"] == filters["status"]]

    columns = [
        {"label": "Purchase Order", "fieldname": "purchase_order", "fieldtype": "Link", "options": "Purchase Order","width":260},
        {"label": "Purchase Receipt", "fieldname": "purchase_receipt", "fieldtype": "Link", "options": "Purchase Receipt","width":160},
        {"label": "Item", "fieldname": "item_code", "fieldtype": "Link", "options": "Item","width":260},
        {"label": "Ordered Qty", "fieldname": "ordered_qty", "fieldtype": "Float","width":150},
        {"label": "Received Qty", "fieldname": "received_qty", "fieldtype": "Float","width":150},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data","width":260}
    ]

    return columns, data
