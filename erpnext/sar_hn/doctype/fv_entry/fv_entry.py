# Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class FVEntry(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		cancellation_reason: DF.SmallText | None
		date_of_emission: DF.Date
		document_type: DF.Literal["01 - INVOICE", "02 - SALES RECEIPT", "03 - RENT RECEIPT", "04 - PROFESSIONAL FEES RECEIPT", "05 - WITHHOLDING CERTIFICATE", "06 - CREDIT NOTE", "07 - DEBIT NOTE", "08 - DELIVERY NOTE"]
		fiscal_number: DF.Data | None
		is_cancelled: DF.Check
		print_authorization: DF.Link | None
		transaction_date: DF.Date
		voucher_no: DF.DynamicLink
		voucher_type: DF.Link
	# end: auto-generated types
	pass
