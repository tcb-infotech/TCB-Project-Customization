import frappe
from frappe import _
from frappe.utils import get_datetime

@frappe.whitelist()
def mark_bulk_attendance(data):
	import json

	if isinstance(data, str):
		data = json.loads(data)
	data = frappe._dict(data)
	if not data.unmarked_days:
		frappe.throw(_("Please select a date."))
		return

	for date in data.unmarked_days:
		doc_dict = {
			"doctype": "Attendance",
			"employee": data.employee,
			"attendance_date": get_datetime(date),
            "custom_project":data.custom_project,
			"status": data.status,
		}
		attendance = frappe.get_doc(doc_dict).insert()
		attendance.submit()