import frappe
from frappe import _
from strategic_gears_cms_site_api.utils import error_response, success_response

@frappe.whitelist(allow_guest=True)
def get_site_map(kwargs):
    try:
        if kwargs.get("type") == "category":
            return category_urls()
        if kwargs.get("type") == "sub-category":
            return sub_category_urls()
        if kwargs.get("type") == "reports":
            return reports_urls()
        if kwargs.get("type") == "corporate_news":
            return corporate_news_urls()
    except Exception as e:
        frappe.logger("Site Map").exception(e)
        return error_response(e)    


def category_urls(with_product=False):
    categories = frappe.get_all("Category", {"slug":["is","set"]},["slug","name"])
    CATEGORIES = {row.name: row.slug for row in categories}
    result = [generate_urls([category]) for category in CATEGORIES.values()]
    return result

def sub_category_urls():
    parent_categories = frappe.get_all("Category", {"slug":["is","set"],"is_group":["is","set"]},["slug","name"])
    result = []
    for parent_category in parent_categories:
        parent_slug = parent_category.slug
        SUB_CATEGORIES  = frappe.get_all("Category", {"slug":["is","set"],"old_parent":parent_category.name, "parent_category":["is","set"]},["slug", "name"])
        CATEGORIES = {row.name: row.slug for row in SUB_CATEGORIES}
        urls = [generate_urls([parent_slug, category]) for category in CATEGORIES.values()]
        result.extend(urls)
    return result
    
def reports_urls():
    reports_master = frappe.get_all("Reports Master", {"slug":["is","set"]},["slug","name"])
    result = []
    parent_slug = "providers/reports"
    REPORT = {row.name: row.slug for row in reports_master}
    urls = [generate_urls([parent_slug, report]) for report in REPORT.values()]
    result.extend(urls)
    return result

def corporate_news_urls():
    corporate_news_articles = frappe.get_all("Corporate News Articles", {"slug":["is","set"]},["slug","name"])
    result = []
    parent_slug = "about/corporate-news"
    ARTICLES = {row.name: row.slug for row in corporate_news_articles}
    urls = [generate_urls([parent_slug, article]) for article in ARTICLES.values()]
    result.extend(urls)
    return result

def generate_urls(path_elements):
    #elements: list of elements of path
    filtered_path_elements = [element for element in path_elements if element is not None]
    return '/' + '/'.join(filtered_path_elements)  