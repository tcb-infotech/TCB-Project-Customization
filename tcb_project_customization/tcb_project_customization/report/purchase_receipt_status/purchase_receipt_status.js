frappe.query_reports["Purchase Receipt Status"] = {
	"filters": [
	  {
		label: "Purchase Order",
		fieldname: "po",
		fieldtype: "Link",
		options: "Purchase Order"
	  },
	  {
		label: "Item",
		fieldname: "item_code",
		fieldtype: "Link",
		options: "Item"
	  },
	  {
		label: "From Date",
		fieldname: "from_date",
		fieldtype: "Date"
	  },
	  {
		label: "To Date",
		fieldname: "to_date",
		fieldtype: "Date"
	  },
	  {
		label: "Status",
		fieldname: "status",
		fieldtype: "Select",
		options: ["", "Pending", "Completed"],
		default: ""
	  }
	]
  };
  