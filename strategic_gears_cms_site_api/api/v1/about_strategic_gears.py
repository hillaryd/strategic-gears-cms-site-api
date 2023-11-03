import frappe
from strategic_gears_cms_site_api.utils import success_response, error_response,translate_keys

@frappe.whitelist(allow_guest=True)
def get_about_strategic_gears(kwargs):
    try:
        data = {}
        user_language = kwargs.get('language')
        doc = frappe.get_doc('About Strategic Gears')
        banner_data = frappe.db.get_list('Banner',
                                    filters={'name': doc.banner},
                                    fields=['banner_name','banner_text','banner_background_image']
                                    )
        data['banner_data'] = banner_data[0]
    
        data['overview_data'] = {'overview_heading': doc.overview_heading,
                               'overview_description': doc.overview_description
                               }
        data['overview_data']['overview_values'] = []

        for item in doc.organizational_purpose_and_values:
            overview_value = {
                'value_heading': item.heading,
                'value_description': item.description
            }
            data['overview_data']['overview_values'].append(overview_value)


        data['services_data'] = {'services_heading': doc.services_heading,
                               'services_description': doc.services_sub_heading
                               }
        
        data['services_data']['services_list'] = []

        for item in doc.services_list:
            service_data = frappe.get_all('Service Details',
                                    filters={'parent': item.services_list},
                                    fields=['service_detail'],
                                    )
            service_master = frappe.get_list('Services Master',
                                    filters={'name': item.services_list},
                                    fields=['slug'],
                                    )
            for service in service_master:
                slug = service.slug
            service_values = []
            for service_value in service_data:
                service_values.append(service_value['service_detail'])
            service = {
                'service_heading': item.services_list,
                'slug':slug,
                'service_values': service_values
            }
            data['services_data']['services_list'].append(service)


        data['reasons_to_choose_us'] = {
            'reasons_to_choose_us_heading': doc.why_choose_us_heading,
            'reasons_to_choose_us_description': doc.why_choose_us_sub_heading
        }

        data['reasons_to_choose_us']['reasons_to_choose_us_list'] = []

        for reason in doc.reasons_to_choose_us:
            data['reasons_to_choose_us']['reasons_to_choose_us_list'].append(reason.reason)

        data['achievements_data']= {
            'achievements_text': ''
        }


        data['achievements_data']['achievements_list_images'] = []

        for image in doc.achievement_images:
            data['achievements_data']['achievements_list_images'].append(image.image)


        data['articles_data'] = []
        
        for article_name in doc.articles:
            articles = frappe.db.get_list('Articles',
                                    filters={'name': article_name.article},
                                    fields=['image','article_name','date','article_url']
                                    )
            
            for article in articles:
                article_date = article['date'].strftime('%d-%m-%y')
                article_data = {
                    'article_image': article['image'],
                    'article_name': article['article_name'],
                    'article_date': article_date,
                    'article_url' : article['article_url']
                }
                data['articles_data'].append(article_data)


        translated_data = translate_keys(data, user_language)
        
        return success_response(data=translated_data) 
    except Exception as e:
        frappe.logger("Token").exception(e)
        return error_response(e)
