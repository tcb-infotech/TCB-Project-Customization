
// frappe.ui.form.on('Purchase Invoice', {

//     onload: function (frm) {
//         if (frm.doc.custom_payment_entry) {
//             if (frm.doc.status == 'Unpaid' || frm.doc.status == 'Overdue' || frm.doc.status == 'Partly Paid') {
//                 frm.add_custom_button('Payment Entry', () => {
//                     let d = new frappe.ui.Dialog({
//                         title: 'Payment Entry',
//                         fields: [
//                             {
//                                 label: 'Mode of Payment',
//                                 fieldname: 'mode_of_payment',
//                                 fieldtype: 'Link',
//                                 options: 'Mode of Payment',
//                                 onchange: () => toggle_party_field()
//                             },
//                             {
//                                 label: 'Payment Type',
//                                 fieldname: 'payment_type',
//                                 fieldtype: 'Select',
//                                 options: ['Receive', 'Pay', 'Internal Transfer'],
//                                 onchange: () => toggle_party_field()
//                             },
//                             {
//                                 label: 'Party Type',
//                                 fieldname: 'party_type',
//                                 fieldtype: 'Link',
//                                 options: 'Party Type',
//                                 hidden: false,
//                                 default: 'Supplier',
//                                 onchange: () => toggle_party_field()
//                             },
//                             {
//                                 label: 'Party',
//                                 fieldname: 'party',
//                                 fieldtype: 'Dynamic Link',
//                                 options: 'party_type',
//                                 default: frm.doc.supplier,
//                                 hidden: true
//                             },
//                             {
//                                 label: 'Company Bank Account',
//                                 fieldname: 'company_bank_account',
//                                 fieldtype: 'Link',
//                                 options: 'Bank Account',
//                                 get_query: () => {
//                                     return {
//                                         filters: {
//                                             'is_company_account': 'Yes',
//                                             'company': 'HRC'
//                                         }
//                                     }
//                                 },
//                                 hidden: true,
//                             },
//                             {
//                                 label: 'Party Bank Account',
//                                 fieldname: 'party_bank_account',
//                                 fieldtype: 'Link',
//                                 options: 'Bank Account',
//                                 get_query: () => {
//                                     return {
//                                         filters: {
//                                             'is_company_account': 'No',
//                                             'party_type': d.fields_dict.party_type.get_value()
//                                         }
//                                     }
//                                 },
//                                 hidden: true,
//                             },
//                             {
//                                 label: 'Account Paid To',
//                                 fieldname: 'account_paid_to',
//                                 fieldtype: 'Link',
//                                 options: 'Account',
//                                 default: frm.doc.credit_to,
//                                 hidden: false,
//                                 get_query: () => {
//                                     if (d.get_value('payment_type') == 'Internal Transfer') {
//                                         return {
//                                             filters: [
//                                                 ['account_type', 'in', ['Bank', 'Cash']],
//                                                 ['company', '=', 'HRC']
//                                             ]
//                                         }
//                                     }
//                                 }
//                             },
//                             {
//                                 label: 'Account Paid From',
//                                 fieldname: 'account_paid_from',
//                                 fieldtype: 'Link',
//                                 options: 'Account',
//                                 hidden: false,
//                                 get_query: () => {
//                                     if (d.get_value('payment_type') == 'Internal Transfer') {
//                                         return {
//                                             filters: [
//                                                 ['account_type', 'in', ['Bank', 'Cash']],
//                                                 ['company', '=', 'HRC']
//                                             ]
//                                         }
//                                     }
//                                 }
//                             },
//                             {
//                                 label: 'Amount Paid',
//                                 fieldname: 'amount_paid',
//                                 fieldtype: 'Currency',
//                                 default: frm.doc.outstanding_amount
//                             },
//                             {
//                                 label: 'Amount Received',
//                                 fieldname: 'amount_received',
//                                 fieldtype: 'Currency',
//                                 hidden: true
//                             }
//                         ],
//                         primary_action_label: 'Submit',
//                         primary_action(values) {

//                             console.log(values)
//                             frappe.call({
//                                 method: 'tcb_project_customization.doc_events.custom_purchase_invoice.make_payment_entry',
//                                 args: {
//                                     values: values,
//                                     doc: frm.doc,
//                                 }
//                             })
//                             d.hide()
//                         }
//                     })

//                     function toggle_party_field() {
//                         let mode_of_payment = d.get_value('mode_of_payment')
//                         let payment_type = d.get_value('payment_type');
//                         let party_type = d.get_value('party_type');

//                         if (mode_of_payment != 'Cash') {
//                             d.fields_dict.company_bank_account.df.hidden = false
//                             d.fields_dict.party_bank_account.df.hidden = false
//                         }
//                         else if (mode_of_payment === 'Cash') {
//                             d.fields_dict.company_bank_account.df.hidden = true
//                             d.fields_dict.party_bank_account.df.hidden = true
//                         }

//                         if ((payment_type === 'Receive' || payment_type === 'Pay') && party_type) {
//                             d.fields_dict.party.df.hidden = false;
//                         }
//                         else if (payment_type == 'Internal Transfer') {
//                             d.fields_dict.party.df.hidden = true;
//                             d.fields_dict.party_type.df.hidden = true;
//                         }
//                         else if (payment_type != 'Internal Transfer') {
//                             d.fields_dict.party.df.hidden = false;
//                             d.fields_dict.party_type.df.hidden = false;
//                         }

//                         else {
//                             d.fields_dict.party.df.hidden = true;
//                         }

//                         if (payment_type === 'Internal Transfer') {
//                             d.fields_dict.amount_received.df.hidden = false
//                         }
//                         else {
//                             d.fields_dict.amount_received.df.hidden = true
//                         }
//                         d.refresh();
//                     }
//                     d.show()
//                 })
//             }
//         }
//     }
// });