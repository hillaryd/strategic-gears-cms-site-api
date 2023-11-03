import frappe
from strategic_gears_cms_site_api.utils import success_response, error_response,translate_keys

@frappe.whitelist(allow_guest=True)
def get_pod(kwargs):
    try:
        user_language = kwargs.get('language')
        data={}
        doc=frappe.get_doc("Points of Difference")
        banner_list=frappe.db.get_list("Banner",filters={"name":doc.banner},fields=["banner_name","banner_text","banner_background_image"]) 
        banner = banner_list[0]
        data["banner_data"]=banner

        image = frappe.get_all("Partners Section Image",fields=["partners_section_image"])
        data["partners_data"]={
            "partners_heading": doc.partners_section_heading,
            "partners_description": doc.partners_section_subheading,
            "partners_imgs": image
        }
    
        data["resource_data"] = {  
            "resource_heading": doc.resource_management_section_heading,
            "resource_description": doc.resource_management_section_description
        }

        business = frappe.get_all("Understanding Bussiness Section",fields=["business_name","business_count"])
        data["understanding_business_data"]={
            "business_section_heading": doc.understanding_bussiness_section_heading,
            "business_section_description": doc.understanding_bussiness_section_description,
             "businesses_list": business


        }
        data["framework_data"]= {
            "framework_heading": doc.frameworks_heading,
            "framework_description": doc.frameworks_description,
            }

        translated_data = translate_keys(data, user_language)
        return success_response(data=translated_data)
    
    except Exception as e:
        frappe.logger("Token").exception(e)
        return error_response(e)
