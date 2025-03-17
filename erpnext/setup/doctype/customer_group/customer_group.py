# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import frappe
from frappe import _
from frappe.utils.nestedset import NestedSet, get_root_of


class CustomerGroup(NestedSet):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		account: DF.Link | None
		advance_account: DF.Link | None
		bypass_credit_limit_check: DF.Check
		company: DF.Link
		credit_limit: DF.Currency
		customer_group_name: DF.Data
		default_price_list: DF.Link | None
		is_group: DF.Check
		lft: DF.Int
		old_parent: DF.Link | None
		parent_customer_group: DF.Link | None
		payment_terms: DF.Link | None
		rgt: DF.Int
	# end: auto-generated types

	nsm_parent_field = "parent_customer_group"

	def validate(self):
		if not self.parent_customer_group:
			self.parent_customer_group = get_root_of("Customer Group")
		self.validate_currency_for_receivable_and_advance_account()

	def validate_currency_for_receivable_and_advance_account(self):
		receivable_account_currency = None
		advance_account_currency = None
		if self.account:
			receivable_account_currency = frappe.get_cached_value(
				"Account", self.account, "account_currency"
			)

		if self.advance_account:
			advance_account_currency = frappe.get_cached_value(
				"Account", self.advance_account, "account_currency"
			)

		if (
			receivable_account_currency
			and advance_account_currency
			and receivable_account_currency != advance_account_currency
		):
			frappe.throw(
				_(
					"Both Receivable Account: {0} and Advance Account: {1} must be of same currency for company: {2}"
				).format(
					frappe.bold(self.account),
					frappe.bold(self.advance_account),
					frappe.bold(self.company),
				)
			)

	def on_update(self):
		super().on_update()
		self.validate_one_root()


def get_parent_customer_groups(customer_group):
	lft, rgt = frappe.db.get_value("Customer Group", customer_group, ["lft", "rgt"])

	return frappe.db.sql(
		"""select name from `tabCustomer Group`
		where lft <= %s and rgt >= %s
		order by lft asc""",
		(lft, rgt),
		as_dict=True,
	)


def on_doctype_update():
	frappe.db.add_index("Customer Group", ["lft", "rgt"])
