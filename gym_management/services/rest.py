import frappe



@frappe.whitelist()
def redirect_user_to_dashboard():
    # if frappe.session.user not in ["Administrator", "Guest"]:
        frappe.local.response["home_page"] = "/app/gym_navigation"