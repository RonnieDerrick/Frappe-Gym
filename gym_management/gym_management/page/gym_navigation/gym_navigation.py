import frappe
from frappe.utils import today, date_diff

@frappe.whitelist()
def get_member_profile():
	user = frappe.session.user

	# 1. Find Gym Member linked to this user
	member = frappe.get_value("Gym Member", {"email": user}, ["name", "full_name"], as_dict=True)
	if not member:
		frappe.logger().info(f"No Gym Member linked to user: {user}")
		return None

	# 2. Active membership
	membership = frappe.db.get_value(
		"Gym Membership",
		{
			"member": member.name,
			"start_date": ("<=", today()),
			"end_date": (">=", today())
		},
		["membership_type", "end_date"],
		as_dict=True
	)

	# 3. Remaining days
	remaining_days = date_diff(membership.end_date, today()) if membership else 0

	# 4. Trainer Subscription
	subscription = frappe.db.get_value(
		"Gym Trainer Subscription",
		{"member": member.name},
		"trainer"
	)

	trainer = None
	if subscription:
		# Safe trainer lookup with fallback if email or phone_number missing
		try:
			trainer_fields = ["full_name", "email", "phone_number"]
			trainer = frappe.db.get_value("Gym Trainer", subscription, trainer_fields, as_dict=True)
		except Exception as e:
			frappe.logger().error(f"Error fetching Gym Trainer '{subscription}': {str(e)}")
			trainer = None

	# 5. Past memberships
	past = frappe.get_all(
		"Gym Membership",
		filters={"member": member.name, "end_date": ("<", today())},
		fields=["membership_type", "start_date", "end_date"],
		order_by="start_date desc"
	)

	# 6. Return final payload
	return {
		"member": member,
		"membership": membership,
		"trainer": trainer,
		"remaining_days": remaining_days,
		"past": past
	}
