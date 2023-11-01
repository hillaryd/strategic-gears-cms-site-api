import frappe
from strategic_gears_cms_site_api.utils import success_response, error_response,translate_keys

@frappe.whitelist(allow_guest=True)
def get_team_member(kwargs):
    try:
        user_language = kwargs.get('language')
        banner = frappe.get_all("Banner", filters= {"banner_name": "OUR TEAM"}, fields=["banner_name","banner_text_image","banner_background_image"])
        banner_data = banner[0]



        team = frappe.get_all("Team Member", pluck="name")
        team_member = []

        for single_member in team:
            team_member_dict = {}
            
            speciality = frappe.get_all("Speciality Details", filters={"parent":single_member},
                                        pluck="speciality_name")
            
            doc= frappe.get_doc("Team Member", single_member)
            team_member_image = doc.image
            team_member_name = doc.employee_name
            team_member_designation = doc.designation
            team_member_description = doc.description

            team_member_dict = {"team_member_image":team_member_image, 
                                "team_member_name":team_member_name,
                                "team_member_designation":team_member_designation,
                                "team_member_speciality": speciality,
                                "team_member_description":team_member_description
                                }
            team_member.append(team_member_dict)

        data = {"banner_data":banner_data, "team_members_data":team_member}
        translated_data = translate_keys(data, user_language)
        return success_response(data=translated_data)
    except Exception as e:
        frappe.logger("Team").exception(e)
        return error_response(e)