import frappe


def validate(self, *args, **kwargs):

    # Unique SuperVisors
    details_set = set()
    unique_details = []

    for row in self.custom_supervisor_details:
        if row.supervisor_id not in details_set:
            unique_details.append(row)
            details_set.add(row.supervisor_id)

    self.custom_supervisor_details = []
    for row in unique_details:
        self.append("custom_supervisor_details",row)
    
    # Unique Gang Leader
    details_set = set()
    unique_details = []

    for row in self.custom_gang_leader_details:
        if row.gang_leader_id not in details_set:
            unique_details.append(row)
            details_set.add(row.gang_leader_id)


    self.custom_gang_leader_details = []
    for row in unique_details:
        self.append("custom_gang_leader_details",row)
    
    # Unique WatchMen
    details_set = set()
    unique_details = []
    
    for row in self.custom_watchmen_details:
        if row.watchman_id not in details_set:
            unique_details.append(row)
            details_set.add(row.watchman_id)

    self.custom_watchmen_details = []
    for row in unique_details:
        self.append("custom_watchmen_details",row)

    details_set = set()
    unique_details = []


def after_insert(doc, method):

# get_doc is used for two purposed, to fetch existing documents or create a new document
# When you pass a dictionary of values with the 'doctype' key, 
# it creates a new document instance but does not save it until you call .insert() or .save()
    parent_warehouse_doc= frappe.get_doc({
        'doctype':'Warehouse',
        'warehouse_name':doc.project_name,
        'custom_project':doc.name, 
        "company":doc.company,
        'is_group': 1,
    })

    parent_warehouse_doc.insert()

    
    store_warehouse_doc= frappe.get_doc({
        'doctype':'Warehouse',
        'warehouse_name':f"{doc.project_name}-Store",
        'custom_project':doc.name, 
        "company":doc.company,
        'parent_warehouse': parent_warehouse_doc.name
    })

    store_warehouse_doc.insert()



    frappe.msgprint("Warehouse Successfully Created")