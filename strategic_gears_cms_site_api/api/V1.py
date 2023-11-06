import frappe
from strategic_gears_cms_site_api.utils import success_response, error_response
import strategic_gears_cms_site_api.api.v1.access_token as access_token
import strategic_gears_cms_site_api.api.v1.navbar as navbar
import strategic_gears_cms_site_api.api.v1.about_strategic_gears as about_strategic_gears
import strategic_gears_cms_site_api.api.v1.navbar as navbar
import strategic_gears_cms_site_api.api.v1.team_member as team_member
import strategic_gears_cms_site_api.api.v1.client as client
import strategic_gears_cms_site_api.api.v1.point_of_difference as point_of_difference
import strategic_gears_cms_site_api.api.v1.color_accounting as color_accounting
import strategic_gears_cms_site_api.api.v1.services as services
import strategic_gears_cms_site_api.api.v1.newsletter as newsletter
import strategic_gears_cms_site_api.api.v1.report as report
import strategic_gears_cms_site_api.api.v1.corporate_news as corporate_news
import strategic_gears_cms_site_api.api.v1.home as home
import strategic_gears_cms_site_api.api.v1.seo as seo
import strategic_gears_cms_site_api.api.v1.contact as contact


class V1():
    def __init__(self):
        self.methods = {
            'access_token':['get_access_token'],
            'navbar':['get_data'],
            'about_strategic_gears':['get_about_strategic_gears'],
            'navbar':['get_navbar_data'],
            'team_member':['get_team_member','home_page_team_member'],
            'client':['get_client'],
            'point_of_difference':['get_pod'],
            'color_accounting':['get_color_accounting'],
            'services':['get_service_details','get_service_list'],
            'newsletter':['get_newsletter'],
            'report':['get_report_list','report_details','home_page_report_list'],
            'corporate_news':['get_corporate_news_data','get_corporate_news_article_details'],
            'home':['get_introduction','get_home_banner'],
            'seo':['get_site_map'],
            'contact':['create_contact']
        }

    def class_map(self, kwargs):
        entity = kwargs.get('entity')
        method = kwargs.get('method')
        if self.methods.get(entity):
            if method in self.methods.get(entity):
                function = f"{kwargs.get('entity')}.{kwargs.get('method')}({kwargs})"
                return eval(function)
            else:
                return error_response("Method Not Found!")
        else:
            return error_response("Entity Not Found!")