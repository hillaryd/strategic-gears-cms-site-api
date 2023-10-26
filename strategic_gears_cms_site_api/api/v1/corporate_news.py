import frappe
from strategic_gears_cms_site_api.utils import success_response, error_response

@frappe.whitelist(allow_guest=True)
def get_corporate_news_data(kwargs):
    corporate_news = frappe.get_all("Banner", filters={"banner_name": "CORPORATE NEWS"}, fields=["banner_name", "banner_text_image"])
    corporate_news_articles = frappe.get_all("Corporate News Articles", fields=["article_heading", "article_image", "article_description"])

    data_req = {
        "banner_data": {
            "banner_name":"",
            "banner_txt_image": "",
            "banner_background_img": "",
        },
        "corporate_articles_list": []
    }
    banner_field = frappe.get_doc("Banner", corporate_news[0].banner_name)
    data_req["banner_data"]["banner_name"] = banner_field.banner_name
    data_req["banner_data"]["banner_txt_image"] = banner_field.banner_text_image
    data_req["banner_data"]["banner_background_img"] = banner_field.banner_background_image
    for article in corporate_news_articles:
        data_req["corporate_articles_list"].append({
            "article_name": article["article_heading"],
            "article_image": article["article_image"],  
            "description": article["article_description"]
        })

    return data_req

@frappe.whitelist(allow_guest=True)
def get_corporate_news_article_details(kwargs):
    corporate_news_article = kwargs.get("article")
    article = frappe.get_doc("Corporate News Articles", corporate_news_article)
    banner_data = {}
    if article.banner:
        banner_field = frappe.get_doc("Banner", article.banner)
        banner_data = {
            "banner_name":banner_field.banner_name,
            "banner_text_img": banner_field.banner_text_image,
            "banner_background_img": banner_field.banner_background_image,
        }
    
    data_req = {
        "banner_data": banner_data,
        "corporate_article_data": {
            "article_name": article.article_heading,
            "Article Description":article.article_description,
            "Article Image":article.article_image,
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
    return data_req
