import time

import frappe

from strategic_gears_cms_site_api.api.V1 import V1
from strategic_gears_cms_site_api.utils import error_response, success_response


@frappe.whitelist(allow_guest=True)
def api(**kwargs):
	try:
		st = time.time()
		version = kwargs.get("version")
		if version == "v1":
			api = V1()
		elif version == "v2":
			api = "V2"
		response = api.class_map(kwargs)
		et = time.time()
		if type(response) == dict:
			response["exec_time"] = f"{round(et - st, 4)} seconds"
		return response
	except Exception as e:
		frappe.logger("registration").exception(e)
		return error_response(e)
