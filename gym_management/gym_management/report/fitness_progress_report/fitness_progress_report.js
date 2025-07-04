// Copyright (c) 2025, Kiprono Derrick and contributors
// For license information, please see license.txt

frappe.query_reports["Fitness Progress Report"] = {
  "filters": [
    {
      "fieldname": "member",
      "label": "Gym Member",
      "fieldtype": "Link",
      "options": "Gym Member",
      "reqd": 1
    }
  ]
};

