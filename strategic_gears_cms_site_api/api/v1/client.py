import frappe
from strategic_gears_cms_site_api.utils import success_response, error_response

@frappe.whitelist(allow_guest=True)
def get_client(kwargs):
    try:
        doc = frappe.get_doc("Client")
        banner_data_list = frappe.get_all("Banner",filters={"banner_name":"OUR CLIENTS"},fields=["banner_name","banner_image"])
        banner_data = banner_data_list[0]
        clients = frappe.get_all("Client Details",pluck="client_name") 
        client_data_list = []
        for client in clients:
            client_img = frappe.get_all("Client Master",filters={"client_name":client},fields=["client_image"])
            client_data_list.append(client_img)
        client_data=[]
        def removeNestings(l):
            for i in l:
                if type(i) == list:
                    removeNestings(i)
                else:
                    client_data.append(i)
        removeNestings(client_data_list)
        data={"banner_data":banner_data,"client_data":client_data}
        return success_response(data)
    except Exception as e:
        frappe.logger("Client").exception(e)
        return error_response(e)