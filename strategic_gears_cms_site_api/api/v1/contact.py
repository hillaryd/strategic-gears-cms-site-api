import frappe
from sme_sg.utils import success_response, error_response
import json

def create_contact(kwargs):
    try:
        if frappe.request.data:
            request_data = json.loads(frappe.request.data)
            email = request_data.get("email")
            first_name = request_data.get("first_name")
            last_name = request_data.get("last_name")
            contacts = frappe.get_list("Contact",filters = {"first_name":first_name,"last_name":last_name},fields=['name'])
            for contact in contacts:
            # Check if email already exists in child table
                existing_contact = frappe.get_all("Contact Email", filters={"parent": contact.name, "email_id": email})
                if existing_contact:
                    return error_response("Contact with this email already exists.")
            doc = frappe.new_doc("Contact")
            doc.update({
                "first_name": first_name,
                "last_name": last_name
            })
            
            doc.append(
                "email_ids",
                {
                    "doctype": "Contact Email",
                    "email_id": email
                },
            )
            doc.insert(ignore_permissions=True)
            return success_response(data=f'Contact created successfully!!')
    except Exception as e:
        frappe.logger("contact").exception(e)
        return error_response(str(e))

