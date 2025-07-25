app_name = "tcb_project_customization"
app_title = "TCB Project Customization"
app_publisher = "AjayRaj Mahiwal"
app_description = "TCB Project Customization"
app_email = "support@tcbinfotech.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "tcb_project_customization",
# 		"logo": "/assets/tcb_project_customization/logo.png",
# 		"title": "TCB Project Customization",
# 		"route": "/tcb_project_customization",
# 		"has_permission": "tcb_project_customization.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/tcb_project_customization/css/tcb_project_customization.css"
# app_include_js = "/assets/tcb_project_customization/js/tcb_project_customization.js"

# include js, css files in header of web template
# web_include_css = "/assets/tcb_project_customization/css/tcb_project_customization.css"
# web_include_js = "/assets/tcb_project_customization/js/tcb_project_customization.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "tcb_project_customization/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
    "Vehicle": "public/js/custom_vehicle.js",
    "Project": "public/js/custom_project.js",
    "Employee": "public/js/custom_employee.js",
    "Vehicle Log": "public/js/custom_vehicle_log.js",
    "Purchase Order": "public/js/custom_po.js",
    "Warehouse": "public/js/custom_warehouse.js",
    'Purchase Invoice':'public/js/custom_purchase_invoice.js',
    'Sales Order':'public/js/custom_sales_order.js',
    'Sales Invoice':'public/js/custom_sales_invoice.js',
    'Quotation':'public/js/custom_quotation.js',
    "Direct Timesheet":"public/js/custom_direct_timesheet.js",
    "Inspection":"public/js/custom_inspection.js",
    "DPR Detail":"public/js/custom_dpr_detail.js",
    "Request for Quotation":"public/js/custom_request_for_quotation.js",
    "Material Receipt":"public/js/custom_material_receipt.js",
    "Delivery Instruction":"public/js/custom_delivery_instruction.js",
    "Cube Test":"public/js/cube_test.js"
}
doctype_list_js = {"Attendance" : "tcb_project_customization/doctype/attendance/attendance_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "tcb_project_customization/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "tcb_project_customization.utils.jinja_methods",
# 	"filters": "tcb_project_customization.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "tcb_project_customization.install.before_install"
# after_install = "tcb_project_customization.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "tcb_project_customization.uninstall.before_uninstall"
# after_uninstall = "tcb_project_customization.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "tcb_project_customization.utils.before_app_install"
# after_app_install = "tcb_project_customization.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "tcb_project_customization.utils.before_app_uninstall"
# after_app_uninstall = "tcb_project_customization.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "tcb_project_customization.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Project": {
		"validate": ["tcb_project_customization.doc_events.project.validate"],
        "after_insert":"tcb_project_customization.doc_events.project.after_insert"
	},
    'Vehicle':{
        'validate':'tcb_project_customization.doc_events.custom_vehicle.validate'
    },
    # "Request for Quotation":{
    #     "on_submit":'tcb_project_customization.doc_events.mail_request_for_quotation.mail_rfq'
    # }
    # "Purchase Order":{
    #     "on_submit":'tcb_project_customization.doc_events.mail_purchase_order.mail_po'
    # }
    # 'Purchase Receipt':{
    #     "on_submit":'tcb_project_customization.doc_events.mail_purchase_receipt.send_purchase_receipt_mail'
    # },
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"tcb_project_customization.tasks.all"
# 	],
	# "daily": [
    #     "tcb_project_customization.doc_events.mail_request_for_quotation.check_subscription_status"
    # ]
# 	"hourly": [
# 		"tcb_project_customization.tasks.hourly"
# 	],
# 	"weekly": [
# 		"tcb_project_customization.tasks.weekly"
# 	],
# 	"monthly": [
# 		"tcb_project_customization.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "tcb_project_customization.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "tcb_project_customization.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "tcb_project_customization.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["tcb_project_customization.utils.before_request"]
# after_request = ["tcb_project_customization.utils.after_request"]

# Job Events
# ----------
# before_job = ["tcb_project_customization.utils.before_job"]
# after_job = ["tcb_project_customization.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"tcb_project_customization.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }



# fixtures=[
#     {
#         "dt": "Role Profile",
#         "filters":[
#             ['name','=','Project Mgt']
#         ]
#     }
# ]