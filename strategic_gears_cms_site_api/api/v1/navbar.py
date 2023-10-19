import frappe
from frappe.utils.password import check_password
from strategic_gears_cms_site_api.utils import success_response, error_response

import frappe
from frappe.utils import get_url

@frappe.whitelist(allow_guest=True)
def get_data(kwargs):
    parent_categories = frappe.get_all("Category", filters={"is_group": 1}, fields=["category_name", "label", "custom_url", "sequence", "slug"])

    navbar_data = []

    for category in parent_categories:
        navbar_item = {
            "name": category.category_name,
            "label": category.label,
            "url": category.custom_url,
            "seq": category.sequence,
            "slug": category.slug,
            "values": []
        }

        child_categories = frappe.get_all("Category", filters={"parent_category": category.category_name}, fields=["category_name", "label", "custom_url", "sequence", "slug"])
        
        for child_category in child_categories:
            child_navbar_item = {
                "name": child_category.category_name,
                "label": child_category.label,
                "url": child_category.custom_url,
                "seq": child_category.sequence,
                "slug": child_category.slug,
                "values": []
            }
            navbar_item['values'].append(child_navbar_item)

        navbar_data.append(navbar_item)

    return navbar_data
