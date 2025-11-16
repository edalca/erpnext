# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


from frappe.model.document import Document
from frappe.contacts.address_and_contact import load_address_and_contact

class Branch(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		abbr: DF.Data | None
		branch: DF.Data
		company: DF.Link
	# end: auto-generated types

	def onload(self):
		load_address_and_contact(self, "branch")
