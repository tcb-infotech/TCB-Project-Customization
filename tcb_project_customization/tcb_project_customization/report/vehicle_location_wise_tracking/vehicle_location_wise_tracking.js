// Copyright (c) 2024, AjayRaj Mahiwal and contributors
// For license information, please see license.txt

frappe.query_reports["Vehicle Location Wise Tracking"] = {
	"filters": [

	],
	onload: function(report) {
        setTimeout(() => {
            // Get the datatable instance
            if (report.datatable && report.datatable.rowmanager) {
                // Collapse all rows
                report.datatable.rowmanager.collapseAllNodes();
                
                // Show expand all button and hide collapse all button
                report.$report.find('[data-action="expand_all_rows"]').show();
                report.$report.find('[data-action="collapse_all_rows"]').hide();
            }
        }, 300);
    },

};
// frappe.query_reports["Vehicle Location Wise Tracking"] = {
//     "filters": [],
    
//     "formatter": function(value, row, column, data, default_formatter) {
//         if (column.fieldname === "location") {
//             value = default_formatter(value, row, column, data);
//             if (data.location) {
//                 value = `<a href="#" onclick="frappe.query_report.show_location_details('${data.location}'); return false;">${value}</a>`;
//             }
//             return value;
//         }
//         return default_formatter(value, row, column, data);
//     },
// };

// frappe.query_report.show_location_details = function(location) {
//     frappe.call({
//         method: "frappe.client.get_list",
//         args: {
//             doctype: "Vehicle",
//             filters: {
//                 "custom_vehicle_location": location
//             },
//             fields: [
//                 "name",
//                 "custom_vehicle_type",
//                 "make",
//                 "model",
//                 "license_plate",
//                 "chassis_no",
//                 "vehicle_status"
//             ]
//         },
//         callback: function(r) {
//             let vehicles = r.message || [];
            
//             // Create a dialog to show vehicle details
//             let d = new frappe.ui.Dialog({
//                 title: __('Vehicles at {0}', [location]),
//                 width: 800,
//                 fields: [{
//                     fieldtype: 'HTML',
//                     fieldname: 'vehicle_details'
//                 }]
//             });
            
//             // Create HTML table for vehicle details
//             let html = `
//                 <div class="table-responsive">
//                     <table class="table table-bordered">
//                         <thead>
//                             <tr>
//                                 <th>${__('Vehicle')}</th>
//                                 <th>${__('Type')}</th>
//                                 <th>${__('Make')}</th>
//                                 <th>${__('Model')}</th>
//                                 <th>${__('License Plate')}</th>
//                                 <th>${__('Chassis No')}</th>
//                                 <th>${__('Status')}</th>
//                             </tr>
//                         </thead>
//                         <tbody>
//             `;
            
//             vehicles.forEach(vehicle => {
//                 html += `
//                     <tr>
//                         <td><a href="#Form/Vehicle/${vehicle.name}">${vehicle.name}</a></td>
//                         <td>${vehicle.custom_vehicle_type || ''}</td>
//                         <td>${vehicle.make || ''}</td>
//                         <td>${vehicle.model || ''}</td>
//                         <td>${vehicle.license_plate || ''}</td>
//                         <td>${vehicle.chassis_no || ''}</td>
//                         <td>${vehicle.vehicle_status || ''}</td>
//                     </tr>
//                 `;
//             });
            
//             html += `
//                         </tbody>
//                     </table>
//                 </div>
//             `;
            
//             d.fields_dict.vehicle_details.$wrapper.html(html);
//             d.show();
//         }
//     });
// };