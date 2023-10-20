import frappe
from strategic_gears_cms_site_api.utils import success_response, error_response

@frappe.whitelist(allow_guest=True)
def get_newsletter(kwargs):
    try:
        data={}
        doc=frappe.get_doc("Monthy NewsLetter")

        banner_list=frappe.db.get_list("Banner",filters={"name":doc.banner},fields=["description","banner_image"]) 
        banner = banner_list[0]
        data["banner_data"]={"banner_text":banner["description"],"banner_image":banner["banner_image"]}
        
        data["newsletters_list"]=[]
        for item in doc.newesletter_master_table:
            service_data = frappe.db.get_list('NewsLetters Master',
                                    filters={'name': item.newsletter_master},
                                    fields=["newsletter_name",'cover_image',"attach"]
                                    )
            newsletter=service_data[0]
            data["newsletters_list"].append({"newsletter_name":newsletter["newsletter_name"],"newsletter_image":newsletter["cover_image"],"newsletter_file":newsletter["attach"]})

        return success_response(data=data)
    
    except Exception as e:
        frappe.logger("Token").exception(e)
        return error_response(e)
