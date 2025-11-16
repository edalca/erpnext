# Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import nowdate


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


def get_auth(emission_point, posting_date):
    auth_list = frappe.get_all("Print Authorization",
        filters={
            "emission_point": emission_point,
            "document_type": "01 - INVOICE",  # Factura
            "status": "Active"
        },
        fields=[
            "name",
            "request_date",
            "expiration_date",
            "authorized_range_start",
            "authorized_range_end"
        ],
        order_by="request_date asc"
    )

    valid_auths = [
        auth for auth in auth_list
        if auth.request_date <= posting_date and auth.expiration_date >= posting_date
    ]

    if not valid_auths:
        frappe.throw(_("No valid Print Authorization found for this Emission Point and posting date."))

    return frappe.get_doc("Print Authorization", valid_auths[0].name)


@frappe.whitelist()
def make_fv_entry(sales_invoice, emission_point):
    existing_fv = frappe.get_all("FV Entry",
        filters={"voucher_no": sales_invoice},
        limit=1
    )

    if existing_fv:
        frappe.throw(_("This Sales Invoice already has a Fiscal Voucher assigned: {0}").format(existing_fv[0].name))

    si = frappe.get_doc("Sales Invoice", sales_invoice)
    pe = frappe.get_doc("Emission Point", emission_point)
    auth = get_auth(emission_point, si.posting_date)
    establishment = frappe.get_doc("Establishment", pe.establishment)
    establishment_series = establishment.series

    # Buscar último correlativo usado con esta autorización
    last_fv = frappe.get_all("FV Entry",
    filters={"print_authorization": auth.name},
    fields=["fiscal_number"],
    order_by="fiscal_number desc",
    limit=1
	)
    if last_fv:
        try:
            last_num = int(last_fv[0].fiscal_number.split("-")[-1])
        except ValueError:
            frappe.throw(_("Last voucher number is not numeric."))
        next_num = last_num + 1
    else:
        next_num = auth.authorized_range_start

    if next_num > auth.authorized_range_end:
        auth.status = "Exhausted"
        auth.save(ignore_permissions=True)
        frappe.throw(_("The Print Authorization has been exhausted. No more vouchers can be issued."))

    correlative = str(next_num).zfill(8)
    doc_type_code = auth.document_type.split(" ")[0]
    fiscal_number = f"{establishment_series}-{pe.series}-{doc_type_code}-{correlative}"

    fv = frappe.new_doc("FV Entry")
    fv.company = pe.company
    fv.establishment = pe.establishment
    fv.emission_point = pe.emission_point_name
    fv.emission_mode = pe.emission_mode
    fv.print_authorization = auth.name
    fv.document_type = auth.document_type
    fv.voucher_type = "Sales Invoice"
    fv.voucher_no = sales_invoice
    fv.date_of_emission = nowdate() 
    fv.transaction_date = si.posting_date
    fv.fiscal_number = fiscal_number
    fv.insert()

    # Marcar como Exhausted si se usó el último número
    if next_num == auth.authorized_range_end:
        auth.status = "Exhausted"
        auth.save(ignore_permissions=True)

    si.db_set("cai", auth.name)
    si.db_set("issue_deadline", auth.expiration_date)
    si.db_set("reception_date", fv.date_of_emission)
    si.db_set("authorized_range", f"{auth.series}")
    si.db_set("correlative", fiscal_number)



    return fv.name
