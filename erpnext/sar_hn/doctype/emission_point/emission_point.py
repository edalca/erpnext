# Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class EmissionPoint(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		amended_from: DF.Link | None
		company: DF.Link
		emission_mode: DF.Literal["M\u00e1quina Registradora", "SFC en Red Fijo", "SFC en Red M\u00f3vil", "SFC Independiente Fijo", "SFC Independiente M\u00f3vil"]
		emission_point_name: DF.Data
		establishment: DF.Link
		series: DF.Data
		status: DF.Literal["Active", "Inactive", "Revoked"]
	# end: auto-generated types
	pass
