// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.ui.form.on("Customer", {
	setup: function (frm) {
		frm.set_query("customer_group", { is_group: 0 });
		frm.set_query("default_price_list", { selling: 1 });
		frm.set_query("default_account", function (doc) {
			return {
				filters: {
					account_type: "Receivable",
					root_type: "Asset",
					company: doc.company,
					is_group: 0,
				},
			};
		});

		frm.set_query("advance_account", function (doc) {
			return {
				filters: {
					account_type: "Receivable",
					root_type: "Liability",
					company: doc.company,
					is_group: 0,
				},
			};
		});

		if (frm.doc.__islocal == 1) {
			frm.set_value("represents_company", "");
		}

		frm.set_query("customer_primary_contact", function (doc) {
			return {
				query: "erpnext.selling.doctype.customer.customer.get_customer_primary_contact",
				filters: {
					customer: doc.name,
				},
			};
		});
		frm.set_query("customer_primary_address", function (doc) {
			return {
				filters: {
					link_doctype: "Customer",
					link_name: doc.name,
				},
			};
		});

		frm.set_query("default_bank_account", function () {
			return {
				filters: {
					is_company_account: 1,
				},
			};
		});

		frm.set_query("user", "portal_users", function () {
			return {
				filters: {
					ignore_user_type: true,
				},
			};
		});

	},
	customer_primary_address: function (frm) {
		if (frm.doc.customer_primary_address) {
			frappe.call({
				method: "frappe.contacts.doctype.address.address.get_address_display",
				args: {
					address_dict: frm.doc.customer_primary_address,
				},
				callback: function (r) {
					frm.set_value("primary_address", r.message);
				},
			});
		}
		if (!frm.doc.customer_primary_address) {
			frm.set_value("primary_address", "");
		}
	},

	is_internal_customer: function (frm) {
		if (frm.doc.is_internal_customer == 1) {
			frm.toggle_reqd("represents_company", true);
		} else {
			frm.toggle_reqd("represents_company", false);
		}
	},

	customer_primary_contact: function (frm) {
		if (!frm.doc.customer_primary_contact) {
			frm.set_value("mobile_no", "");
			frm.set_value("email_id", "");
		}
	},

	loyalty_program: function (frm) {
		if (frm.doc.loyalty_program) {
			frm.set_value("loyalty_program_tier", null);
		}
	},

	refresh: function (frm) {
		if (frappe.defaults.get_default("cust_master_name") != "Naming Series") {
			frm.toggle_display("naming_series", false);
		} else {
			erpnext.toggle_naming_series();
		}

		if (!frm.doc.__islocal) {
			frappe.contacts.render_address_and_contact(frm);

			// custom buttons

			frm.add_custom_button(
				__("Accounts Receivable"),
				function () {
					frappe.set_route("query-report", "Accounts Receivable", {
						party_type: "Customer",
						party: frm.doc.name,
					});
				},
				__("View")
			);

			frm.add_custom_button(
				__("Accounting Ledger"),
				function () {
					frappe.set_route("query-report", "General Ledger", {
						party_type: "Customer",
						party: frm.doc.name,
						party_name: frm.doc.customer_name,
					});
				},
				__("View")
			);

			frm.add_custom_button(
				__("Pricing Rule"),
				function () {
					erpnext.utils.make_pricing_rule(frm.doc.doctype, frm.doc.name);
				},
				__("Create")
			);

			if (cint(frappe.defaults.get_default("enable_common_party_accounting"))) {
				frm.add_custom_button(
					__("Link with Supplier"),
					function () {
						frm.trigger("show_party_link_dialog");
					},
					__("Actions")
				);
			}

			// indicator
			erpnext.utils.set_party_dashboard_indicators(frm);
		} else {
			frappe.contacts.clear_address_and_contact(frm);
		}
		const tax_id=frm.fields_dict["tax_id"].input
		Inputmask('99999999999999').mask(tax_id);
		var grid = cur_frm.get_field("sales_team").grid;
		grid.set_column_disp("allocated_amount", false);
		grid.set_column_disp("incentives", false);
	},
	credit_limit(frm){
		if (frm.doc.credit_limit>0){
			frm.set_df_property("payment_terms","reqd",1)
		}else{
			frm.set_df_property("payment_terms","reqd",0)
		}
	},
	validate: function (frm) {
		if (frm.doc.lead_name) frappe.model.clear_doc("Lead", frm.doc.lead_name);
	},

	show_party_link_dialog: function (frm) {
		const dialog = new frappe.ui.Dialog({
			title: __("Select a Supplier"),
			fields: [
				{
					fieldtype: "Link",
					label: __("Supplier"),
					options: "Supplier",
					fieldname: "supplier",
					reqd: 1,
				},
			],
			primary_action: function ({ supplier }) {
				frappe.call({
					method: "erpnext.accounts.doctype.party_link.party_link.create_party_link",
					args: {
						primary_role: "Customer",
						primary_party: frm.doc.name,
						secondary_party: supplier,
					},
					freeze: true,
					callback: function () {
						dialog.hide();
						frappe.msgprint({
							message: __("Successfully linked to Supplier"),
							alert: true,
						});
					},
					error: function () {
						dialog.hide();
						frappe.msgprint({
							message: __("Linking to Supplier Failed. Please try again."),
							title: __("Linking Failed"),
							indicator: "red",
						});
					},
				});
			},
			primary_action_label: __("Create Link"),
		});
		dialog.show();
	},
});
