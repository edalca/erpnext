// Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on("Establishment", {
    refresh(frm) {
        // Hide address block if the doc is new
        frm.toggle_display("address_html", !frm.is_new());

        if (!frm.is_new()) {
            // Render linked addresses and contacts
            frappe.contacts.render_address_and_contact(frm);
        } else {
            // Clear address/contact blocks for new docs
            frappe.contacts.clear_address_and_contact(frm);

            // Apply input mask to 'series' field (e.g., 000, 001)
            const series = frm.fields_dict["series"].input;
            Inputmask('999').mask(series);
        }
    },
});