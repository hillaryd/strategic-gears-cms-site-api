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


@frappe.whitelist(allow_guest=True)
def get_home_banner(kwargs):
    try:
        home_banner = frappe.get_list("Banner", filters={"name": "HOME"}, fields=['name', 'slug', 'banner_text_image',
                                                                                   'banner_background_image', 'description'])
        if home_banner:
            return success_response(data=home_banner[0])
        else:
            return success_response(data={})

    except Exception as e:
        frappe.logger("Introduction").exception(e)
        return error_response(e)
