import frappe
from strategic_gears_cms_site_api.utils import success_response, error_response,translate_keys

@frappe.whitelist(allow_guest=True)
def get_newsletter(kwargs):
    try:
        user_language = kwargs.get('language')
        data={}
        doc=frappe.get_doc("Monthy NewsLetter")

        banner_list=frappe.db.get_list("Banner",filters={"name":doc.banner},fields=["banner_name","banner_text","banner_background_image","banner_height","banner_font_size","banner_alignment"]) 
        banner = banner_list[0]
        data["banner_data"]={"banner_name":banner["banner_name"],
                            "banner_text":banner["banner_text"],
                            "banner_background_image":banner['banner_background_image'],
                            "banner_height":banner["banner_height"],
                            "banner_font_size":banner["banner_font_size"],
                            "banner_alignment":banner["banner_alignment"],
                            }
        
        data["newsletters_list"]=[]
        for item in doc.newesletter_master_table:
            service_data = frappe.db.get_list('NewsLetters Master',
                                    filters={'name': item.newsletter_master},
                                    fields=["newsletter_name",'cover_image',"attach"]
                                    )
            newsletter=service_data[0]
            data["newsletters_list"].append({"newsletter_name":newsletter["newsletter_name"],"newsletter_image":newsletter["cover_image"],"newsletter_file":newsletter["attach"]})
        translated_data = translate_keys(data, user_language)
        return success_response(data=translated_data)
    
    except Exception as e:
        frappe.logger("Token").exception(e)
        return error_response(e)
