import frappe
from strategic_gears_cms_site_api.utils import success_response, error_response
import strategic_gears_cms_site_api.api.v1.access_token as access_token
import strategic_gears_cms_site_api.api.v1.about_strategic_gears as about_strategic_gears
import strategic_gears_cms_site_api.api.v1.navbar as navbar
import strategic_gears_cms_site_api.api.v1.team_member as team_member

class V1():
    def __init__(self):
        self.methods = {
            'access_token':['get_access_token'],
            'about_strategic_gears':['get_about_strategic_gears'],
            'navbar':['get_navbar_data'],
            'team_member':['get_team_member']
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