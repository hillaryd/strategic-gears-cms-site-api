import frappe
# from frappe.utils.response import build_response

def build_response(status, data=None, message=None):
    response = {
        "status": status
    }
    if data is not None:
        response["data"] = data
    if message is not None:
        response["message"] = message
    return response

@frappe.whitelist(allow_guest=True)
def get_req():
    try:
        response = frappe.db.get_list('Banner',fields=['banner_image', 'seq', 'text', 'button_text', 'button_label', 'button_url'])
        return build_response("success", data=response)
    except Exception as e:
        return build_response("failed", message=e)
        #frappe.log_error(title=_("API Error"), message=e)

        #return build_response("error", message=_("An error occurred while fetching data.")
                              
