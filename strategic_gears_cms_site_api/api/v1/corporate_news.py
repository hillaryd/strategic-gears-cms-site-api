import frappe
from strategic_gears_cms_site_api.utils import success_response, error_response,translate_keys

@frappe.whitelist(allow_guest=True)
def get_corporate_news_data(kwargs):
    try:
        user_language = kwargs.get('language')
        corporate_news = frappe.get_all("Banner", filters={"banner_name": "CORPORATE NEWS"}, fields=["banner_name", "banner_text"])
        corporate_news_articles = frappe.get_all("Corporate News Articles", fields=["article_heading","show_data_on_website","article_image", "article_description","slug"])

        data_req = {
            "banner_data": {
                "banner_name":"",
                "banner_text": "",
                "banner_background_img": "",
            },
            "corporate_articles_list": []
        }
        banner_field = frappe.get_doc("Banner", corporate_news[0].banner_name)
        data_req["banner_data"]["banner_name"] = banner_field.banner_name
        data_req["banner_data"]["banner_text"] = banner_field.banner_text
        data_req["banner_data"]["banner_background_img"] = banner_field.banner_background_image
        for article in corporate_news_articles:
            data_req["corporate_articles_list"].append({
                "article_name": article["article_heading"],
                "slug": article["slug"],
                "article_image": article["article_image"],  
                "description": article["article_description"],
                "show_data_on_website":article["show_data_on_website"]
            })
        translated_data = translate_keys(data_req, user_language)
        return success_response(data=translated_data)
    except Exception as e:
        frappe.logger("Corporate News").exception(e)
        return error_response(e)

@frappe.whitelist(allow_guest=True)
def get_corporate_news_article_details(kwargs):
    try:
        user_language = kwargs.get('language')
        corporate_news_article = kwargs.get("article")
        articles = frappe.get_list("Corporate News Articles", filters={"slug":corporate_news_article},
                fields= ['name','banner','article_heading','article_description','article_image',
                         'section_1_image','section_1_heading','section_1_description','section_2_image',
                         'section_2_heading','section_2_description','section_3_image','section_3_heading','section_3_description'])
        banner_data = {}
        for article in articles:
            if article.banner:
                banner_field = frappe.get_doc("Banner", article.banner)
                banner_data = {
                    "banner_name":banner_field.banner_name,
                    "banner_text": banner_field.banner_text,
                    "banner_background_img": banner_field.banner_background_image,
                }
            
            data_req = {
                "banner_data": banner_data,
                "corporate_article_data": {
                    "article_name": article.article_heading,
                    "article_description":article.article_description,
                    "article_image":article.article_image,
                    "section_1_image": article.section_1_image,
                    "section_1_heading": article.section_1_heading,
                    "section_1_description": article.section_1_description,
                    "section_2_image": article.section_2_image,
                    "section_2_heading": article.section_2_heading,
                    "section_2_description": article.section_2_description,
                    "section_3_image": article.section_3_image,  
                    "section_3_heading": article.section_3_heading,  
                    "section_3_description": article.section_3_description,  
                }
            }
            translated_data = translate_keys(data_req, user_language)
            return success_response(data=translated_data)
    except Exception as e:
        frappe.logger("Corporate News").exception(e)
        return error_response(e)