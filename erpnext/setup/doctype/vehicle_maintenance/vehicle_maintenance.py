# Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class VehicleMaintenance(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from erpnext.setup.doctype.vehicle_maintenance_item.vehicle_maintenance_item import VehicleMaintenanceItem
		from frappe.types import DF

		amended_from: DF.Link | None
		assigned_to: DF.Data
		contact_number: DF.Data | None
		customer: DF.Data
		customer_comment: DF.SmallText
		date: DF.Date
		vehicle: DF.Link
		vehicle_maintenance_item: DF.Table[VehicleMaintenanceItem]
		work_description: DF.SmallText
	# end: auto-generated types
	pass
