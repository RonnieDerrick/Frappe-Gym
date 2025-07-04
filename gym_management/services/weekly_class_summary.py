import frappe
from frappe.utils import today, add_days, nowdate
from frappe.core.doctype.communication.email import make

@frappe.whitelist()
def send_weekly_class_summary():
    members = frappe.get_all("Gym Member", fields=["name", "email", "full_name"])

    for member in members:
        bookings = frappe.get_all("Gym Class Booking",
            filters={
                "member": member.name,
                "class_date": (">=", add_days(today(), -7))
            },
            fields=["gym_class", "class_date"],
            order_by="class_date desc"
        )

        if bookings:
            rows = "".join([f"<li>{b.gym_class} - {b.booking_date}</li>" for b in bookings])
            body = f"""
                <p>Hi {member.full_name},</p>
                <p>Here’s your weekly class attendance summary:</p>
                <ul>{rows}</ul>
                <p>Keep it up! 💪</p>
            """

            frappe.sendmail(
                recipients=[member.email],
                subject="Your Weekly Gym Class Summary",
                message=body
            )
