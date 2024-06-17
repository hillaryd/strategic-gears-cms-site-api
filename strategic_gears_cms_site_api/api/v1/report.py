import frappe

from strategic_gears_cms_site_api.utils import error_response, success_response, translate_keys


@frappe.whitelist(allow_guest=True)
def get_report_list(kwargs):
	try:
		user_language = kwargs.get("language")
		reports = frappe.get_list(
			"Reports Master",
			fields=[
				"label",
				"name",
				"banner",
				"heading",
				"image",
				"slug",
				"custom_image_ar",
				"custom_attach_report_ar",
				"show_on_website",
				"sequence",
			],
			order_by="sequence",
		)
		data_req = {"banner_data": {}, "reports_list": []}

		banner_field = frappe.get_doc("Banner", reports[0].banner)
		data_req["banner_data"]["banner_name"] = banner_field.banner_name
		data_req["banner_data"]["banner_text"] = banner_field.banner_text
		data_req["banner_data"]["banner_background_image"] = banner_field.banner_background_image
		data_req["banner_data"]["banner_height"] = banner_field.banner_height
		data_req["banner_data"]["banner_font_size"] = banner_field.banner_font_size
		data_req["banner_data"]["banner_alignment"] = banner_field.banner_alignment

		for report in reports:
			if user_language == "en" and report.image != None:
				report_info = {
					"report_name": report.heading,
					"label": report.label,
					"report_image": report.image,
					"slug": report.slug,
					"sequence": report.sequence,
				}
				data_req["reports_list"].append(report_info)
			if user_language == "ar" and report.custom_image_ar != None:
				report_info = {
					"report_name": report.heading,
					"label": report.label,
					"report_image": report.custom_image_ar,
					"slug": report.slug,
					"sequence": report.sequence,
				}
				data_req["reports_list"].append(report_info)
		translated_data = translate_keys(data_req, user_language)
		return success_response(data=translated_data)
	except Exception as e:
		frappe.logger("Report_list").exception(e)
		return error_response(e)


@frappe.whitelist(allow_guest=True)
def report_details(kwargs):
	try:
		user_language = kwargs.get("language")
		report_name = kwargs.get("name")
		reports = frappe.get_list(
			"Reports Master",
			filters={"slug": report_name},
			fields=[
				"label",
				"name",
				"heading",
				"description",
				"attach_report",
				"image",
				"custom_image_ar",
				"custom_attach_report_ar",
				"show_on_website",
				"sequence",
			],
		)
		for report in reports:
			if not report:
				return {"error": "Report not found"}
			if user_language == "en" and report.image != None:
				report_detail = {
					"report_name": report.heading,
					"label": report.label,
					"report_image": report.image,
					"report_description": report.description,
					"report_file": report.attach_report,
					"sequence": report.sequence,
					"other_reports": [],
				}
			if user_language == "ar" and report.custom_image_ar != None:
				report_detail = {
					"report_name": report.heading,
					"label": report.label,
					"report_image": report.custom_image_ar,
					"report_description": report.description,
					"report_file": report.custom_attach_report_ar,
					"sequence": report.sequence,
					"other_reports": [],
				}

			other_reports = frappe.get_all(
				"Other Publications For Reports",
				filters={"parent": report.name},
				fields=["other_publications"],
			)

			for other_report in other_reports:
				other_report_doc = frappe.get_doc("Reports Master", other_report.other_publications)
				if other_report_doc:
					if user_language == "en" and other_report_doc.image != None:
						report_detail["other_reports"].append(
							{
								"report_name": other_report_doc.heading,
								"label": other_report_doc.label,
								"report_image": other_report_doc.image,
								"slug": other_report_doc.slug,
								"sequence": other_report_doc.sequence,
							}
						)
					if user_language == "ar" and other_report_doc.custom_image_ar != None:
						report_detail["other_reports"].append(
							{
								"report_name": other_report_doc.heading,
								"label": other_report_doc.label,
								"report_image": other_report_doc.custom_image_ar,
								"slug": other_report_doc.slug,
								"sequence": other_report_doc.sequence,
							}
						)
			translated_data = translate_keys(report_detail, user_language)
			return success_response(data=translated_data)
	except Exception as e:
		frappe.logger("Report_list").exception(e)
		return error_response(e)


@frappe.whitelist(allow_guest=True)
def home_page_report_list(kwargs):
	try:
		user_language = kwargs.get("language")
		reports = frappe.get_list(
			"Reports Master",
			filters={"show_on_website": 1},
			fields=[
				"label",
				"name",
				"banner",
				"heading",
				"image",
				"slug",
				"custom_image_ar",
				"custom_attach_report_ar",
				"show_on_website",
				"home_page_sequence",
			],
			order_by="home_page_sequence",
		)
		result = {"reports_list": []}
		for report in reports:
			if user_language == "en" and report.image != None:
				report_info = {
					"report_name": report.heading,
					"label": report.label,
					"report_image": report.image,
					"slug": report.slug,
					"show_on_website": report.show_on_website,
					"home_page_sequence": report.home_page_sequence,
				}
				result["reports_list"].append(report_info)
			if user_language == "ar" and report.custom_image_ar != None:
				report_info = {
					"report_name": report.heading,
					"label": report.label,
					"report_image": report.custom_image_ar,
					"slug": report.slug,
					"show_on_website": report.show_on_website,
					"home_page_sequence": report.home_page_sequence,
				}
				result["reports_list"].append(report_info)
		translated_data = translate_keys(result, user_language)
		return success_response(data=translated_data)
	except Exception as e:
		frappe.logger("Report list").exception(e)
		return error_response(e)
