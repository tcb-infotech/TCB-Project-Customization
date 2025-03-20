import frappe

# @frappe.whitelist()
# def rentStockEntry(item,qnt,rate,twarehouse):
#     se= frappe.new_doc("Stock Entry")
#     se.stock_entry_type= "Material Transfer",
    
#     se.append("items",{
#         "s_warehouse":"Rent Items - TCB",
#         "t_warehouse":twarehouse,
#         "item_code":item,
#         "qty":qnt,
#         "basic_rate":rate
#     })

#     se.save()
#     se.submit()
    
#     return se.name()