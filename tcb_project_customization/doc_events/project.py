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


def after_insert(doc, method=None):
    if not frappe.db.exists("Warehouse", {"warehouse_name": f"{doc.project_name}-Store"}):
        store_warehouse_doc = frappe.new_doc("Warehouse")
        store_warehouse_doc.warehouse_name = f"{doc.project_name}-Store"
        store_warehouse_doc.custom_project = doc.name
        store_warehouse_doc.company = doc.company
        store_warehouse_doc.save()

    frappe.msgprint("Warehouse Successfully Created")