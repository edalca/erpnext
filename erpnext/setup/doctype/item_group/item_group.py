# Copyright (c) 2021, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

import copy

import frappe
from frappe import _
from frappe.utils.nestedset import NestedSet
from frappe.model.naming import set_name_from_naming_options

class ItemGroup(NestedSet):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from erpnext.stock.doctype.item_default.item_default import ItemDefault
        from erpnext.stock.doctype.item_tax.item_tax import ItemTax
        from frappe.types import DF

        abbr: DF.Data | None
        buying_cost_center: DF.Link | None
        company: DF.Link
        default_discount_account: DF.Link | None
        default_price_list: DF.Link | None
        default_provisional_account: DF.Link | None
        default_supplier: DF.Link | None
        default_warehouse: DF.Link | None
        deferred_expense_account: DF.Link | None
        deferred_revenue_account: DF.Link | None
        expense_account: DF.Link | None
        image: DF.AttachImage | None
        income_account: DF.Link | None
        is_group: DF.Check
        item_group_defaults: DF.Table[ItemDefault]
        item_group_name: DF.Data
        item_tax_template: DF.Link | None
        lft: DF.Int
        maximum_net_rate: DF.Float
        minimum_net_rate: DF.Float
        old_parent: DF.Link | None
        parent_item_group: DF.Link | None
        rgt: DF.Int
        selling_cost_center: DF.Link | None
        tax_category: DF.Link | None
        taxes: DF.Table[ItemTax]
        valid_from: DF.Date | None
    # end: auto-generated types

    def autoname(self):
        self.name = self.item_group_name + "-" + self.abbr

    def on_update(self):
        # Actualizar el name si item_group_name o abbr cambiaron
        new_name = self.item_group_name + "-" + self.abbr
        if self.name != new_name:
            frappe.rename_doc(self.doctype, self.name, new_name, force=True)
            self.name = new_name  # Actualizar el name en el documento actual

        # Ejecutar las operaciones de NestedSet y otras validaciones
        NestedSet.on_update(self)
        self.validate_one_root()
        self.delete_child_item_groups_key()

    def validate(self):
        if not self.parent_item_group and not frappe.flags.in_test:
            if frappe.db.exists("Item Group", _("All Item Groups")):
                self.parent_item_group = _("All Item Groups")
        self.validate_item_group_defaults()
        self.check_item_tax()

    def check_item_tax(self):
        """Check whether Tax Rate is not entered twice for same Tax Type"""
        check_list = []
        for d in self.get("taxes"):
            if d.item_tax_template:
                if (d.item_tax_template, d.tax_category) in check_list:
                    frappe.throw(
                        _("{0} entered twice {1} in Item Taxes").format(
                            frappe.bold(d.item_tax_template),
                            f"for tax category {frappe.bold(d.tax_category)}" if d.tax_category else "",
                        )
                    )
                else:
                    check_list.append((d.item_tax_template, d.tax_category))

    def on_trash(self):
        NestedSet.on_trash(self, allow_root_deletion=True)
        self.delete_child_item_groups_key()

    def delete_child_item_groups_key(self):
        frappe.cache().hdel("child_item_groups", self.name)

    def validate_item_group_defaults(self):
        from erpnext.stock.doctype.item.item import validate_item_default_company_links

        validate_item_default_company_links(self.item_group_defaults)


def get_child_item_groups(item_group_name):
    item_group = frappe.get_cached_value("Item Group", item_group_name, ["lft", "rgt"], as_dict=1)

    child_item_groups = [
        d.name
        for d in frappe.get_all(
            "Item Group", filters={"lft": (">=", item_group.lft), "rgt": ("<=", item_group.rgt)}
        )
    ]

    return child_item_groups or {}


def get_item_group_defaults(item, company):
    item = frappe.get_cached_doc("Item", item)
    item_group = frappe.get_cached_doc("Item Group", item.item_group)

    for d in item_group.item_group_defaults or []:
        if d.company == company:
            row = copy.deepcopy(d.as_dict())
            row.pop("name")
            return row

    return frappe._dict()
