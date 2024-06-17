import json

import frappe

from strategic_gears_cms_site_api.utils import error_response, success_response

# def create_inquiry(kwargs):
#     try:
#         if frappe.request.data:
#             request_data = json.loads(frappe.request.data)
#             company_email = request_data.get("company_email")
#             email_context = {
#                 'full_name': request_data.get("full_name"),
#                 'email_address': request_data.get("email_address"),
#                 'mobile_number': request_data.get("mobile_number"),
#                 'inquiry_message': request_data.get("inquiry_message")
#             }
#             return send_mail("New Inquiry", [company_email], email_context)
#     except Exception as e:
#         frappe.logger("Email").exception(e)
#         return error_response(e)


def create_inquiry(kwargs):
	try:
		if frappe.request.data:
			request_data = json.loads(frappe.request.data)
			website_inquiry = frappe.new_doc("Website Inquiry")
			website_inquiry.full_name = request_data.get("full_name")
			website_inquiry.email_id = request_data.get("email_address")
			website_inquiry.mobile_number = request_data.get("mobile_number")
			website_inquiry.inquiry_message = request_data.get("inquiry_message")
			website_inquiry.save()
			return success_response({"docname": website_inquiry.name})
	except Exception as e:
		frappe.logger("Email").exception(e)
		return error_response(e)


def send_mail(template_name, recipients, context):
	try:
		frappe.sendmail(
			recipients=recipients,
			subject=frappe.render_template(
				frappe.db.get_value("Email Template", template_name, "subject"),
				context,
			),
			message=frappe.render_template(
				frappe.db.get_value("Email Template", template_name, "response"),
				context,
			),
		)
		return success_response("Email Sent")
	except Exception as e:
		frappe.logger("Email").exception(e)
		return error_response(e)
