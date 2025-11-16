# Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe import _
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
		emission_point_name: DF.Data | None
		establishment: DF.Link
		series: DF.Data
		status: DF.Literal["Active", "Inactive", "Revoked"]
	# end: auto-generated types

	def autoname(self):
		"""Generate the document name using establishment, series, and emission_mode."""
		if self.establishment and self.series and self.emission_mode:
			self.name = f"{self.establishment} - {self.series} - Auto Impresor: {self.emission_mode}"


	def validate(self):
		self.set_emission_point_name()
		self.validate_unique_emission_point_name()

	def set_emission_point_name(self):
		"""Generate the emission_point_name based on establishment, series, and emission_mode."""
		if self.series and self.emission_mode:
			self.emission_point_name = f"{self.series} - Auto Impresor: {self.emission_mode}"

	def validate_unique_emission_point_name(self):
		"""Ensure the generated emission_point_name is unique within the same company."""
		if self.emission_point_name and self.company:
			existing = frappe.db.exists("Punto de Emision", {
                "emission_point_name": self.emission_point_name,
                "company": self.company
            })
			if existing and existing != self.name:
				frappe.throw(
                    _("An Emission Point with the name '{0}' already exists for this company.").format(self.emission_point_name)
                )

