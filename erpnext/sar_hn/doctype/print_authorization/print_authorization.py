# Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class PrintAuthorization(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		amended_from: DF.Link | None
		authorized_range_end: DF.Int
		authorized_range_start: DF.Int
		cai: DF.Data
		company: DF.Link
		document_type: DF.Literal["01 - INVOICE", "02 - SALES RECEIPT", "03 - RENT RECEIPT", "04 - PROFESSIONAL FEES RECEIPT", "05 - WITHHOLDING CERTIFICATE", "06 - CREDIT NOTE", "07 - DEBIT NOTE", "08 - DELIVERY NOTE"]
		emission_point: DF.Link
		establishment: DF.Link
		expiration_date: DF.Date
		quantity: DF.Int
		request_date: DF.Date
		series: DF.Data | None
		status: DF.Literal["", "Active", "Expired", "Exhausted", "Revoked"]
	# end: auto-generated types
	def validate(self):
			# Validar rango autorizado
			if self.authorized_range_start > self.authorized_range_end:
				frappe.throw(_("Authorized Range Start cannot be greater than Authorized Range End"))

			# Validar fechas
			if self.request_date and self.expiration_date:
				if self.request_date > self.expiration_date:
					frappe.throw(_("Request Date cannot be after Expiration Date"))

			# Calcular cantidad
			if self.authorized_range_start and self.authorized_range_end:
				self.quantity = self.authorized_range_end - self.authorized_range_start + 1
	def before_save(self):
		# Validar campos necesarios
		if not self.establishment or not self.emission_point or not self.document_type:
			frappe.throw(_("Establishment, Emission Point, and Document Type are required to generate the series."))

		# Obtener códigos
		est_code = frappe.db.get_value("Establishment", self.establishment, "series")
		ep_code = frappe.db.get_value("Emission Point", self.emission_point, "series")
		doc_code = self.document_type.split(" - ")[0] if " - " in self.document_type else self.document_type

		# Validar correlativos
		if not self.authorized_range_start or not self.authorized_range_end:
			frappe.throw(_("Authorized range start and end are required."))

		# Formatear correlativos
		start_num = str(self.authorized_range_start).zfill(8)
		end_num = str(self.authorized_range_end).zfill(8)

		# Construir series completa
		prefix = f"{est_code.zfill(3)}-{ep_code.zfill(3)}-{doc_code.zfill(2)}"
		self.series = f"{prefix}-{start_num} / {prefix}-{end_num}"
