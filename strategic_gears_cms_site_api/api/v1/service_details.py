import frappe
from strategic_gears_cms_site_api.utils import success_response, error_response

@frappe.whitelist(allow_guest=True)
def get_service_details(kwargs):
    try:
        services = frappe.get_list("Services Master",pluck="name")
        banner=[]
        data = []
        details = []
        service_list=[]
        for service in services:
            banner = frappe.get_list("Banner",filters={"name":service},fields=["banner_name","banner_image"])
            for b in banner:
                banner_data = b
            service_details_list = frappe.get_all("Service Details",filters={"parent":service},pluck="service_detail")
            service_detail = []
            for service_details in service_details_list:
                get_service_details = frappe.get_all("Service Details Master",filters={"name":service_details},fields=["heading","description"])
                service_detail.append(get_service_details[0])
            service_desc = frappe.get_list("Services Master",filters={"name":service},pluck="description")
            for service in service_desc:
                desc = service
            details = {"banner_data":banner_data,"description":desc,"services_list":service_detail}
           
            data.append(details)
        return success_response(data)
    except Exception as e:
        frappe.logger("Service_Details").exception(e)
        return error_response(e)