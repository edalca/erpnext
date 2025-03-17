// Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on("Stock Setting", {
	setup(frm) {
		frm.set_query("default_warehouse", function (doc) {
			return {
				filters: [["company", "=", doc.company]],
			};
		});
		frm.set_query("sample_retention_warehouse", function (doc) {
			return {
				filters: [["company", "=", doc.company]],
			};
		});
		frm.set_query("item_group", function (doc) {
			return {
				filters: [["company", "=", doc.company]],
			};
		});
	},
	refresh(frm) {},
});
