import frappe
from strategic_gears_cms_site_api.utils import success_response, error_response
import json

def create_inquiry(kwargs):
    try:
        if frappe.request.data:
            request_data = json.loads(frappe.request.data)
            company_email = request_data.get("company_email")
            email_context = {
                'full_name': request_data.get("full_name"),
                'email_address': request_data.get("email_address"),
                'mobile_number': request_data.get("mobile_number"),
                'inquiry_message': request_data.get("inquiry_message")
            }
            return send_mail("New Inquiry", [company_email], email_context)
    except Exception as e:
        frappe.logger("Email").exception(e)
        return error_response(e)    

def send_mail(template_name, recipients, context):
    try:
        frappe.sendmail(
            recipients=recipients,
            subject=frappe.render_template(
                frappe.db.get_value(
                    "Email Template", template_name, "subject"
                ),
                context,
            ),
            message=frappe.render_template(
                frappe.db.get_value(
                    "Email Template", template_name, "response"
                ),
                context,
            ),
        )
        return success_response("Email Sent")
    except Exception as e:
        frappe.logger("Email").exception(e)
        return error_response(e)
