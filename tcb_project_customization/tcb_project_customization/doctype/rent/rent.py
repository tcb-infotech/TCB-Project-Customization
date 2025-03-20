# Copyright (c) 2025, AjayRaj Mahiwal and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc


class Rent(Document):
    pass

     

@frappe.whitelist()
def makeStockEntry(rentItem,warehouse,quantity,rateuom, customer,uom):
	se= frappe.new_doc("Delivery Note")
	se.customer= customer
	se.set_warehouse= warehouse

	se.append("items", {
    "item_code": rentItem,
    "qty": quantity,
    "uom":uom,
    "rate": rateuom
})

	se.save()
	se.submit()
	return se.name



# get_mapped_doc(source_doctype, source_name, table_mapping, ignore_permissions=False, ignore_child_tables=False)

# source_doctype → The Doctype from which we are copying data.
# source_name → The name (ID) of the document we want to copy from.
# table_mapping → A dictionary defining how fields are copied from the source document to the target document.
# ignore_permissions → If True, bypasses user permissions.
# ignore_child_tables → If True, skips copying child tables.

@frappe.whitelist()
def returnStockEntry(dname):
    dn = get_mapped_doc("Delivery Note", dname, {
        "Delivery Note": {
            "doctype": "Delivery Note",
            "field_map": {
                "customer": "customer",
                "set_warehouse": "Rented Items - TCB",
                "company": "company"
            }
        },
        "Delivery Note Item": {
            "doctype": "Delivery Note Item",
            "field_map": {
                "item_code": "item_code",
                "uom": "uom",
                "rate": "rate"
            }
        }
    }, ignore_permissions=True)

    dn.is_return = 1
    dn.return_against = dname

    for item in dn.items:
        item.qty = -abs(item.qty)  

    dn.insert()
    dn.submit()

    return dn.name  


