# gym_management/gym_management/report/most_booked_group_classes/most_booked_group_classes.py

import frappe
from frappe import _

def execute(filters=None):
    columns = [
        {"label": "Group Class", "fieldname": "class_type", "fieldtype": "Data", "width": 200},
        {"label": "Total Bookings", "fieldname": "total", "fieldtype": "Int", "width": 150}
    ]

    data = frappe.db.sql("""
        SELECT class_type, COUNT(*) AS total
        FROM `tabGym Class Booking`
        GROUP BY class_type
        ORDER BY total DESC
    """, as_dict=True)

    return columns, data, None, get_chart(data), get_report_summary(data)


def get_chart(data):
    return {
        "data": {
            "labels": [d["class_type"] for d in data],
            "datasets": [{
                "name": "Bookings",
                "values": [d["total"] for d in data]
            }]
        },
        "type": "bar",
        "colors": ["#7366ff"]
    }


def get_report_summary(data):
    total_bookings = sum(d["total"] for d in data)

    top_class = data[0]["class_type"] if data else "N/A"
    top_count = data[0]["total"] if data else 0

    return [
        {
            "label": "Total Group Class Bookings",
            "value": total_bookings,
            "indicator": "Blue"
        },
        {
            "label": "Top Booked Class",
            "value": f"{top_class} ({top_count})",
            "indicator": "Green"
        }
    ]
