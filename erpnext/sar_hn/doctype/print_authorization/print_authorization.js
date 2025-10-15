// Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on("Print Authorization", {
    onload: function (frm) {
        frm.set_query("establishment", function (doc) {
            return {
                filters: [
                    ['company', "=", doc.company]
                ]
            };
        });
        frm.set_query("emission_point", function (doc) {
            return {
                filters: [
                    ['establishment', "=", doc.establishment]
                ]
            };
        });
    },
    authorized_range_start: function (frm) {
        calculate_quantity(frm);
    },
    authorized_range_end: function (frm) {
        calculate_quantity(frm);
    }

});
function calculate_quantity(frm) {
    if (frm.doc.authorized_range_start && frm.doc.authorized_range_end) {
        let start = frm.doc.authorized_range_start;
        let end = frm.doc.authorized_range_end;
        if (start <= end) {
            frm.set_value('quantity', end - start + 1);
        } else {
            frm.set_value('quantity', null);
        }
    } else {
        frm.set_value('quantity', null);
    }
}
