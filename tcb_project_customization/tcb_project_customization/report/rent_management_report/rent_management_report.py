import frappe

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"label": "Voucher", "fieldname": "name", "fieldtype": "Link", "options": "Rent", "width": 120},
        {"label": "Customer", "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "width": 180},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 100},
        {"label": "Rent Date", "fieldname": "start_date", "fieldtype": "Date", "width": 120},
        {"label": "Rent From", "fieldname": "warehouse", "fieldtype": "Link", "options": "Warehouse", "width": 200},
        {"label": "Rent Item", "fieldname": "rent_item", "fieldtype": "Link", "options": "Item", "width": 280},
        {"label": "Quantity", "fieldname": "quantity", "fieldtype": "Float", "width": 120},
        {"label": "Rate/UOM", "fieldname": "rateuom", "fieldtype": "Float", "width": 120},
        {"label": "Interest Rate", "fieldname": "interest_rate", "fieldtype": "Float", "width": 120},
        {"label": "Total Amount", "fieldname": "total_amount", "fieldtype": "Float", "width": 120},
        {"label": "Returned Quantity", "fieldname": "returned_quantity", "fieldtype": "Float", "width": 120},
        {"label": "Returned To", "fieldname": "return_to", "fieldtype": "Link", "options": "Warehouse", "width": 200}
    ]

def get_data(filters):
    conditions = []
    values = {}

    # Apply filter for customer if selected
    if filters.get("customer"):
        conditions.append("r.customer = %(customer)s")
        values["customer"] = filters["customer"]

    # Apply date range filters - Modified to use start_date for both conditions
    if filters.get("start_date"):
        conditions.append("r.start_date >= %(start_date)s")
        values["start_date"] = filters["start_date"]

    if filters.get("end_date"):
        conditions.append("r.start_date <= %(end_date)s")  # Changed from r.end_date to r.start_date
        values["end_date"] = filters["end_date"]

    # Add warehouse filter
    if filters.get("warehouse"):
        conditions.append("ri.warehouse = %(warehouse)s")
        values["warehouse"] = filters["warehouse"]

    # Add rent item filter
    if filters.get("rent_item"):
        conditions.append("ri.rent_item = %(rent_item)s")
        values["rent_item"] = filters["rent_item"]

    # Add status filter
    if filters.get("status"):
        conditions.append("r.status = %(status)s")
        values["status"] = filters["status"]

    # Add amount range filters
    if filters.get("min_amount"):
        conditions.append("(ri.quantity * ri.rateuom) + ((ri.interest_rate / 100) * ri.quantity * ri.rateuom) >= %(min_amount)s")
        values["min_amount"] = filters["min_amount"]

    if filters.get("max_amount"):
        conditions.append("(ri.quantity * ri.rateuom) + ((ri.interest_rate / 100) * ri.quantity * ri.rateuom) <= %(max_amount)s")
        values["max_amount"] = filters["max_amount"]

    # Construct WHERE clause dynamically
    where_clause = " AND ".join(conditions) if conditions else "1=1"

    raw_data = frappe.db.sql(f"""
    SELECT
        ri.name AS row_id,  -- Ensure uniqueness for child table rows
        r.name AS parent,
        r.name,
        r.customer,
        r.status,
        r.start_date,
        ri.warehouse,
        ri.rent_item,
        ri.quantity,
        ri.rateuom,
        ri.interest_rate,
        (ri.quantity * ri.rateuom) + ((ri.interest_rate / 100) * ri.quantity * ri.rateuom) AS total_amount,
        ri.returned_quantity,
        ri.return_to
    FROM `tabRent Item` ri
    JOIN `tabRent` r ON r.name = ri.parent
    WHERE {where_clause}
    ORDER BY r.creation ASC
""", values, as_dict=True)


    return raw_data