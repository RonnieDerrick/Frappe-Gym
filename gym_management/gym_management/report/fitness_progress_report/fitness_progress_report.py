# Copyright (c) 2025, Kiprono Derrick and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import flt


def execute(filters=None):
    if not filters.member:
        frappe.throw("Please select a Gym Member.")

    data = frappe.get_all(
        "Fitness Tracker",
        filters={"member": filters.gym_member},
        fields=["date", "weightkg", "calories_intake", "body_fat_"],
        order_by="member"
    )

    columns = [
        {"label": "Date", "fieldname": "date", "fieldtype": "Date", "width": 100},
        {"label": "Weight (kg)", "fieldname": "weightkg", "fieldtype": "Float", "width": 120},
        {"label": "Calories", "fieldname": "calories_intake", "fieldtype": "Float", "width": 120},
        {"label": "Body Fat %", "fieldname": "body_fat_", "fieldtype": "Float", "width": 120},
    ]

    chart = {
        "data": {
            "labels": [d["date"] for d in data],
            "datasets": [
                {
                    "name": "Weight (kg)",
                    "values": [flt(d["weightkg"]) for d in data],
                },
                {
                    "name": "Calories",
                    "values": [flt(d["calories_intake"]) for d in data],
                },
                {
                    "name": "Body Fat %",
                    "values": [flt(d["body_fat_"]) for d in data],
                }
            ]
        },
        "type": "line",
        "height": 300
    }

    return columns, data, None, chart
