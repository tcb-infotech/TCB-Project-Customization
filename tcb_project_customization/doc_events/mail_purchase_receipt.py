import frappe

@frappe.whitelist()
def send_purchase_receipt_mail(doc,method):
    pr = doc

    # Get PO Number (assumes all items from one PO)
    po_no = pr.items[0].purchase_order if pr.items else "N/A"

    items_data = []
    for item in pr.items:
        po_item_doc = frappe.get_doc("Purchase Order Item", item.purchase_order_item)
        items_data.append({
            "item_code": item.item_code,
            "item_name": item.item_name,
            "ordered_qty": po_item_doc.qty,
            "received_qty": item.qty,
            "uom": item.uom
        })

    # Render template with context
    email_template = frappe.render_template("templates/includes/purchase_receipt_summary.html", {
        "po_no": po_no,
        "items": items_data
    })

    # Collect recipients from child table
    to = []
    cc = []
    # bcc = []

    for row in pr.custom_email:
        if row.send_as == "To":
            to.append(row.email)
        elif row.send_as == "CC":
            cc.append(row.email)
        # elif row.send_as == "BCC":
        #     bcc.append(row.email)

    # Send mail
    frappe.sendmail(
        recipients=to,
        cc=cc,
        subject=f"Goods Receipt for Purchase Order {po_no}",
        message=email_template
    )
