import frappe
from frappe import _

def execute(filters=None):
    columns = [
        {"label": "Month", "fieldname": "month", "fieldtype": "Data", "width": 150},
        {"label": "Revenue", "fieldname": "revenue", "fieldtype": "Currency", "width": 150}
    ]

    data = frappe.db.sql("""
        SELECT 
            DATE_FORMAT(start_date, '%b %Y') AS month,
            SUM(amount_paid) AS revenue
        FROM `tabGym Membership`
        WHERE docstatus = 1
        GROUP BY YEAR(start_date), MONTH(start_date)
        ORDER BY YEAR(start_date), MONTH(start_date)
    """, as_dict=True)

    # Chart
    chart = {
        "data": {
            "labels": [row["month"] for row in data],
            "datasets": [
                {
                    "name": "Revenue",
                    "values": [row["revenue"] for row in data]
                }
            ]
        },
        "type": "bar",  # or "line"
        "colors": ["#00AEEF"]
    }

    # Summary row
    total = sum(row["revenue"] for row in data)
    summary = [
        {
            "label": "Total Revenue",
            "value": total,
            "indicator": "green"
        }
    ]

    return columns, data, None, chart, summary
