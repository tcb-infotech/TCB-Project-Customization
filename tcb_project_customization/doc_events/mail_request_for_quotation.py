import frappe
@frappe.whitelist()
def mail_rfq(doc, method):
    # If doc is passed as a string (from hooks), convert it to a document
    if isinstance(doc, str):
        doc = frappe.get_doc("Request for Quotation", doc)
    
    if doc.suppliers and doc.items:
        for supplier in doc.suppliers:
            if supplier.email_id and supplier.send_email:
                try:
                    # Get attachments from the document
                    attachments = []
                    # Get attachments from File Attachment table if it exists
                    for attachment in frappe.get_all("File",
                                                   fields=["name", "file_name", "file_url"],
                                                   filters={"attached_to_doctype": "Request for Quotation",
                                                           "attached_to_name": doc.name}):
                        file_doc = frappe.get_doc("File", attachment.name)
                        attachments.append({
                            "fname": file_doc.file_name,
                            "fcontent": file_doc.get_content()
                        })
                    
                    # Prepare CC recipients
                    cc = []
                    if hasattr(doc, 'custom_cc') and doc.custom_cc:
                        cc = doc.custom_cc.split(',') if ',' in doc.custom_cc else [doc.custom_cc]
                    
                    # Render the subject with Jinja
                    subject_template = "{{doc.custom_subject if doc.custom_subject else 'Request for Quotation - " + doc.name + "'}}"
                    subject = frappe.render_template(subject_template, {"doc": doc, "supplier": supplier})
                    
                    # Email message template
                    message_template = """
                     Greetings {{supplier.supplier}},<br/>
                    {{doc.message_for_supplier if doc.message_for_supplier else 'We would like to request a quotation for these mentioned items below-'}}<br/>
                     <table width='100%' border='1'>
                     <tr>
                     <td>S.No</td>
                     <td>Item</td>
                     <td>QTY</td>
                     <td>UOM</td>
                     <td>Drawing No</td>
                     </tr>
                     {% for item in doc.items%}
                     <tr>
                     <td>{{loop.index}}</td>
                     <td>{{item.item_code}}</td>
                     <td>{{item.qty}}</td>
                     <td>{{item.uom}}</td>
                     <td>{{item.custom_drawing_no or ""}}</td>
                     </tr>
                     {%endfor%}
                     </table><br/>
                     {{doc.message_for_supplier}}<br/>
                     {% if doc.terms%}
                     Terms and Conditions -<br/>
                     {{doc.terms}}
                     {%endif%}<br/>
                     Thanks and regards,<br/>
                     {{doc.company}}
                    """
                    
                    # Render the message with Jinja
                    message = frappe.render_template(message_template, {"doc": doc, "supplier": supplier})
                    
                    # Send email
                    frappe.sendmail(
                        recipients=[supplier.email_id],
                        cc=cc,
                        subject=subject,
                        attachments=attachments,
                        message=message
                    )
                    
                    frappe.logger().info(f"Email sent to {supplier.email_id} for RFQ {doc.name}")
                except Exception as e:
                    frappe.logger().error(f"Failed to send email to {supplier.email_id}: {str(e)}")