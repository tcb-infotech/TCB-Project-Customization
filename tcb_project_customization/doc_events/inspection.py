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
                "doctype": "Purchase Order Item"
            }
        },
        target_doc=None
    )