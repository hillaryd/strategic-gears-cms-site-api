import frappe
from frappe.utils.password import check_password
from strategic_gears_cms_site_api.utils import success_response, error_response


@frappe.whitelist(allow_guest=True)
def get_navbar_data(kwargs):
    try:
        parent_categories = frappe.get_all("Category", filters={"is_group": 1}, fields=["category_name", "label", "custom_url", "sequence", "slug"],order_by = "sequence")

        navbar_data = []

        for category in parent_categories:
            parent = None
            navbar_item = {
                "name": category.category_name,
                "label": category.label,
                "url": prepare_url(category.slug, parent),
                "seq": category.sequence,
                "slug": category.slug,
                "values": []
            }


            child_categories = frappe.get_all("Category", filters={"parent_category": category.category_name}, fields=["category_name", "label", "custom_url", "sequence", "slug"],order_by = "sequence")
            
            for child_category in child_categories:
                child_navbar_item = {
                    "name": child_category.category_name,
                    "label": child_category.label,
                    "url": prepare_url(child_category.slug,category.slug,),
                    "seq": child_category.sequence,
                    "slug": child_category.slug,
                    "values": []
                }
                navbar_item['values'].append(child_navbar_item)

            navbar_data.append(navbar_item)

        return success_response(data=navbar_data)
    except Exception as e:
        frappe.logger("Navbar").exception(e)
        return error_response(e)



def prepare_url(prefix, parent=None):
    if parent:
        return f"/{parent}/{prefix}"
    else:
        return f"/{prefix}"
