# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate


class Vehicle(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		brand: DF.Link
		chassis_no: DF.Data | None
		color: DF.Data | None
		fuel_type: DF.Literal["Petrol", "Diesel"]
		license_plate: DF.Data | None
		model: DF.Data
		year: DF.Int
	# end: auto-generated types

