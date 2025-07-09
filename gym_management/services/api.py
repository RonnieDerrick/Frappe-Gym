import frappe
from frappe.utils import today

@frappe.whitelist()
def get_dashboard_stats():
    return {
        "active_members": frappe.db.count("Gym Member"),  # remove 'status'
        "active_trainers": frappe.db.count("Gym Trainer"),  # remove 'status'
        "lockers_today": frappe.db.count("Gym Locker Booking", {"start_date": today()}),
        "class_bookings_today": frappe.db.count("Gym Class Booking", {"class_date": today()})
    }