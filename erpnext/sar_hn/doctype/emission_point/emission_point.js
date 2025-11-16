// Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on("Emission Point", {
    onload: function (frm) {
        frm.set_query("establishment", function (doc) {
            return {
                filters: [
                    ['company', "=", doc.company]
                ]
            };
        });
    },
    refresh(frm) {
        if (frm.is_new()) {
            // Apply input mask to 'series' field (e.g., 000, 001)
            const series = frm.fields_dict["series"].input;
            Inputmask('999').mask(series);
        }
    }
});
