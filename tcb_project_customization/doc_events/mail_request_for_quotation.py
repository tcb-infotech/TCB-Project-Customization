# import frappe
# from datetime import datetime

# @frappe.whitelist()
# def mail_rfq(doc, method):
#     if isinstance(doc, str):
#         doc = frappe.get_doc("Request for Quotation", doc)
    
#     if doc.suppliers and doc.items:
#         for supplier in doc.suppliers:
#             if supplier.email_id and supplier.send_email:
                
#                 frappe.sendmail(
#                     recipients=[supplier.email_id],
#                     subject=f"Request for Quotation: {doc.name}",
#                     message=frappe.render_template(
#                         """
#                         <p>Greetings {{ supplier.supplier }},</p>
#                         <p>We would like to request a quotation for these mentioned items below-</p>
#                         <table width='80%' border='1' cellpadding='5' cellspacing='0'>
#                             <tr>
#                                 <th>S.No</th>
#                                 <th>Item</th>
#                                 <th>QTY</th>
#                                 <th>UOM</th>
#                                 <th>Required Date</th>
#                             </tr>
#                             {% for item in doc.items %}
#                             <tr>
#                                 <td style='text-align:centers'>{{ loop.index }}</td>
#                                 <td style='text-align:centers'>{{ item.item_code }}</td>
#                                 <td style='text-align:centers'>{{ item.qty }}</td>
#                                 <td style='text-align:centers'>{{ item.uom }}</td>
#                                 <td style='text-align:centers'>{{ item.schedule_date }}</td>
#                             </tr>
#                             {% endfor %}
#                         </table>
#                         <p>{{ doc.message_for_supplier }}</p>
#                         {% if doc.terms %}
#                         <p>Terms and Conditions:</p>
#                         <p>{{ doc.terms }}</p>
#                         {% endif %}
#                         <p>Best regards,<br>{{ doc.company }}</p>
#                         """,
#                         {"doc": doc, "supplier": supplier}
#                     )
#                 )