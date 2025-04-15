import frappe
from frappe.model.mapper import get_mapped_doc

@frappe.whitelist()
def inspection(doc):
    return get_mapped_doc(
        "Purchase Order",
        doc,
        {
            "Purchase Order":{
                "doctype":"Inspection",
                "validation":{
                    "docstatus":["=",1]
                }
            },
             "Purchase Order Item": {
                "doctype": "Inspection Item",  # your custom child table
                "field_map": {
                    "name": "purchase_order_item",   # optional: link back to PO item
                    "parent": "purchase_order",      # optional: link to PO
                    "item_code": "item_code",
                    "item_name": "item_name",
                    "qty": "qty",
                    "uom": "uom",
                    "custom_drawing_no":"custom_drawing_no"
                }
            }
        },
        target_doc=None
    )