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
});
