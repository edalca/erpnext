# Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
from frappe.contacts.address_and_contact import load_address_and_contact

class Establishment(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		activity_class: DF.Data | None
		activity_section: DF.Data | None
		amended_from: DF.Link | None
		commercial_name: DF.Data
		company: DF.Link
		enee_code: DF.Data | None
		establishment_type: DF.Literal["", "Principal", "Almacen", "Oficina Administrativa", "Planta Productiva", "Sucursal"]
		is_active: DF.Check
		municipal_permit_no: DF.Data | None
		series: DF.Data
	# end: auto-generated types
	def onload(self):
		load_address_and_contact(self, "establishment")
