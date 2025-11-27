import frappe
from frappe.utils import nowdate

def validate(doc,method=None):
    today_dprs = frappe.db.get_all("Direct Timesheet",filters = {"start_date":doc.start_date,"project":doc.project},fields=["name","project","project_name"])
    if len(today_dprs)>0    :
        for entry in today_dprs:
            frappe.throw(msg = "Existing DPR exists for <b>{0}</b> for this date - <b>{1}</b>".format(entry.project_name,entry.name))