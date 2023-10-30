import frappe
from strategic_gears_cms_site_api.utils import success_response, error_response

@frappe.whitelist(allow_guest=True)
def get_introduction(kwargs):
    try:
        data = {}
        introduction_doc = frappe.get_doc('Introduction')
        data['heading'] = introduction_doc.heading
        data['description'] = introduction_doc.description
        data['is_btn_enable'] = introduction_doc.button_enable
        data['btn_label'] = introduction_doc.button_label
        data['btn_url'] = introduction_doc.button_url
        return success_response(data=data)

    except Exception as e:
        frappe.logger("Introduction").exception(e)
        return error_response(e)
