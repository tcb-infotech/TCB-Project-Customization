import frappe
from frappe.model.mapper import get_mapped_doc

@frappe.whitelist()
def delivery_instruction(doc):
    return get_mapped_doc(
        "Purchase Order",
        doc,
        {
            "Purchase Order":{
                "doctype":"Delivery Instruction",
                "validation":{
                    "docstatus":["=",1]
                }   
            },
            "Purchase Order Item":{
                "doctype":"Inspection Item",
                "field_map":{
                    "name":"purchase_order_item",
                    "parent":"purchase_order",
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