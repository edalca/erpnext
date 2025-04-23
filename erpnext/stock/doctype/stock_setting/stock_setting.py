# Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class StockSetting(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		action_if_quality_inspection_is_not_submitted: DF.Literal["Stop", "Warn"]
		action_if_quality_inspection_is_rejected: DF.Literal["Stop", "Warn"]
		allow_existing_serial_no: DF.Check
		allow_from_dn: DF.Check
		allow_from_pr: DF.Check
		allow_internal_transfer_at_arms_length_price: DF.Check
		allow_negative_stock: DF.Check
		allow_partial_reservation: DF.Check
		allow_to_edit_stock_uom_qty_for_purchase: DF.Check
		allow_to_edit_stock_uom_qty_for_sales: DF.Check
		auto_create_serial_and_batch_bundle_for_outward: DF.Check
		auto_indent: DF.Check
		auto_insert_price_list_rate_if_missing: DF.Check
		auto_reserve_serial_and_batch: DF.Check
		auto_reserve_stock_for_sales_order_on_purchase: DF.Check
		clean_description_html: DF.Check
		company: DF.Link | None
		default_warehouse: DF.Link | None
		disable_serial_no_and_batch_selector: DF.Check
		do_not_update_serial_batch_on_creation_of_auto_bundle: DF.Check
		do_not_use_batchwise_valuation: DF.Check
		enable_stock_reservation: DF.Check
		item_group: DF.Link | None
		item_naming_by: DF.Literal["Item Code", "Naming Series"]
		mr_qty_allowance: DF.Float
		naming_series_prefix: DF.Data | None
		over_delivery_receipt_allowance: DF.Float
		over_picking_allowance: DF.Percent
		pick_serial_and_batch_based_on: DF.Literal["FIFO", "LIFO", "Expiry"]
		reorder_email_notify: DF.Check
		role_allowed_to_create_edit_back_dated_transactions: DF.Link | None
		role_allowed_to_over_deliver_receive: DF.Link | None
		sample_retention_warehouse: DF.Link | None
		show_barcode_field: DF.Check
		stock_auth_role: DF.Link | None
		stock_frozen_upto: DF.Date | None
		stock_frozen_upto_days: DF.Int
		stock_uom: DF.Link | None
		update_existing_price_list_rate: DF.Check
		use_naming_series: DF.Check
		use_serial_batch_fields: DF.Check
		valuation_method: DF.Literal["FIFO", "Moving Average", "LIFO"]
	# end: auto-generated types
	pass
