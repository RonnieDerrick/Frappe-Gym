import frappe
import random
import string
from frappe.model.document import Document

class GymMember(Document):
    def after_insert(self):
        frappe.msgprint("✅ after_insert triggered")
        

        # ✅ STEP 1: Create User if needed
        if self.email and not self.gym_user:
            frappe.msgprint(f"📧 Email Provided: {self.email}")
            if not frappe.db.exists("User", self.email):
                password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
                frappe.msgprint("👤 Creating new User")

                user = frappe.get_doc({
                    "doctype": "User",
                    "email": self.email,
                    "first_name": self.full_name,
                    "send_welcome_email": 0,
                    "new_password": password,
                    "roles": [{"role": "Gym Member"}]
                })
                user.insert(ignore_permissions=False)
                self.db_set("gym_user", user.name)

                # ✅ Send welcome email with login link
                login_url = "http://192.168.100.95:8001/login?redirect-to=/app/user"
                try:
                    frappe.sendmail(
                        recipients=[self.email],
                        subject="Welcome to Our Gym!",
                        message=f"""
                            <h3>Welcome {self.full_name}!</h3>
                            <p>Your gym account has been created.</p>
                            <p><strong>Login Email:</strong> {self.email}</p>
                            <p><strong>Temporary Password:</strong> {password}</p>
                            <p>You can now log in and start your fitness journey.</p>
                            <p>
                                <a href="{login_url}" style="background-color:#4CAF50;color:white;padding:10px 15px;text-decoration:none;border-radius:5px;">
                                    👉 Click Here to Log In
                                </a>
                            </p>
                            <br>
                            <p>Regards,<br>The Gym Team</p>
                        """
                    )
                    frappe.msgprint("📬 Welcome email sent.")
                except Exception as e:
                    frappe.log_error(f"Email sending failed: {str(e)}")
                    frappe.msgprint("⚠️ Email sending failed. Check logs.")
            else:
                self.db_set("gym_user", self.email)
                frappe.msgprint("ℹ️ User already exists; gym_user linked.")
        else:
            frappe.msgprint("⚠️ Missing email or user already linked.")


        # ✅ STEP 3: Create ERPNext Customer
        if not frappe.db.exists("Customer", {"customer_name": self.full_name}):
            frappe.msgprint("🧾 Creating ERP Customer")
            customer = frappe.get_doc({
                "doctype": "Customer",
                "customer_name": self.full_name,
                "customer_type": "Individual",
                "customer_group": "Individual",
                "territory": "All Territories",
                "email_id": self.email
            })
            customer.insert(ignore_permissions=True)
            frappe.msgprint(f"✅ ERP Customer created for {self.full_name}")
            
			        # ✅ STEP 4: Assign User Permission (Only access their own Gym Member doc)
        if self.email:
            frappe.msgprint("🔒 Creating User Permission")

            if not frappe.db.exists("User Permission", {
                "user": self.email,
                "allow": "Gym Member",
                "for_value": self.name
            }):
                frappe.get_doc({
                    "doctype": "User Permission",
                    "user": self.email,
                    "allow": "Gym Member",
                    "for_value": self.name,
                    "apply_to_all_doctypes": 0,
                    "applicable_for": "Gym Member"
                }).insert(ignore_permissions=True)

                frappe.msgprint("🔐 User permission added successfully.")
            else:
                frappe.msgprint("ℹ️ User permission already exists.")

