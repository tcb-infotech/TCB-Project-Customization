
# import frappe
# import json

# @frappe.whitelist()
# def make_payment_entry(values,doc):
#     if isinstance(doc,str):
#         doc= json.loads(doc)
#     if isinstance(values,str):
#         values= json.loads(values)
#     payment_entry = frappe.new_doc("Payment Entry")
#     payment_entry.payment_type = values.get('payment_type')
#     if(payment_entry.payment_type!= 'Internal Transfer'):
#         payment_entry.party_type = values.get('party_type')
#         payment_entry.party = values.get('party')
#         payment_entry.posting_date = doc.get('posting_date')
#         payment_entry.paid_from= values.get('account_paid_from')
#         payment_entry.paid_to = values.get('account_paid_to')
#         payment_entry.paid_from_account_currency= "INR"
#         payment_entry.paid_to_account_currency= "INR"
#         payment_entry.mode_of_payment= values.get('mode_of_payment')
#         payment_entry.paid_amount = values.get('amount_paid') 
#         payment_entry.received_amount = values.get('amount_paid')
#         payment_entry.reference_no = doc.get('name')
#         payment_entry.reference_date = doc.get('posting_date')
#         payment_entry.source_exchange_rate='INR'
#         payment_entry.append("references", {
#             "reference_doctype": "Purchase Invoice",
#             "reference_name": doc.get('name'),
#             "allocated_amount": values.get('amount_paid'),
#             'account':values.get('account_paid_to')            
#         })
#         print('-----------------------------------------',payment_entry.difference_amount)

#     elif payment_entry.payment_type=='Internal Transfer':
#         payment_entry.mode_of_payment= values.get('mode_of_payment')
#         payment_entry.paid_from= values.get('account_paid_from')
#         payment_entry.paid_to = values.get('account_paid_to')
#         payment_entry.paid_from_account_currency= "INR"
#         payment_entry.paid_to_account_currency= "INR"
#         payment_entry.paid_amount = values.get('amount_paid')
#         payment_entry.received_amount = values.get('amount_received')

#         payment_entry.reference_no = doc.get('name')
#         payment_entry.reference_date = doc.get('posting_date')


    
    
#     # if(doc.get('taxes')):
#     #     for item in doc.get('taxes'):
#     #         payment_entry.append('taxes',{
#     #             'charge_type':item.get('charge_type'),
#     #             'account_head':item.get('account_head'),
#     #             'rate':item.get('rate'),
#     #             'tax_amount':item.get('tax_amount'),
#     #     })

#     payment_entry.insert()
#     payment_entry.submit()