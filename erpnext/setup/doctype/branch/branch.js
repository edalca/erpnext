// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on("Branch", {
	refresh: function (frm) {
		if (!frm.is_new()) {
			// Render linked addresses and contacts
			frappe.contacts.render_address_and_contact(frm);
		}
	},

});
