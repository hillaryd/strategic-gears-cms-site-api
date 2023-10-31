import frappe
from strategic_gears_cms_site_api.utils import success_response, error_response,translate_keys

@frappe.whitelist(allow_guest=True)
def get_service_list(kwargs):
    try:
        user_language = kwargs.get('language')
        services = frappe.get_list("Services Master",pluck="name",order_by = 'sequence')
        banner=[]
        data = []
        details = []
        service_list=[]
        for service in services:
            banner = frappe.get_list("Banner",filters={"name":service},fields=["banner_background_image","banner_name"])
            for b in banner:
                banner_data = b
            service_details_list = frappe.get_all("Service Details",filters={"parent":service},pluck="service_detail",order_by = 'sequence')
            service_detail = []
            for service_details in service_details_list:
                get_service_details = frappe.get_all("Service Details Master",filters={"name":service_details},fields=["heading","description"])
                service_detail.extend(get_service_details)
            service_desc = frappe.get_list("Services Master",filters={"name":service},fields=["description","slug"],order_by = 'sequence')
            for service in service_desc:
                desc = service
            details = {"name":banner_data["banner_name"],"banner_image":banner_data["banner_background_image"],"slug":desc["slug"],"services_list":service_detail}
           
            data.append(details)
        translated_data = translate_keys(data, user_language)    
        return success_response(translated_data)
    except Exception as e:
        frappe.logger("Service_Details").exception(e)
        return error_response(e)
    
@frappe.whitelist(allow_guest=True)
def get_service_details(kwargs):
    try:
        user_language = kwargs.get('language')
        # Check if the 'name' parameter is provided in kwargs
        if 'name' not in kwargs:
            return error_response("Name parameter is missing")

        service_name = kwargs.get('name')

        # Retrieve specific service details
        banner = frappe.get_list("Banner", filters={"slug": service_name}, fields=["banner_name", "banner_text_image","banner_background_image"])
        banner_data = banner[0] if banner else {}

        service_desc = frappe.get_list("Services Master", filters={"slug": service_name}, fields=['description','name'],order_by = 'sequence')
    
        for d in service_desc:
            desc = d.description if service_desc else ""
            service_details_list = frappe.get_all("Service Details", filters={"parent": d.name}, pluck="service_detail",order_by = 'sequence')
           
        service_detail = []

        for service_details in service_details_list:
            get_service_details = frappe.get_all("Service Details Master", filters={"name": service_details}, fields=["heading", "description"])
        
            service_detail.extend(get_service_details)  # Use extend instead of append
          
        details = {"banner_data": banner_data, "description": desc, "services_list": service_detail}
        translated_data = translate_keys(details, user_language)
        return success_response(translated_data)
    except Exception as e:
        frappe.logger("Specific_Service_Details").exception(e)
        return error_response(e)
