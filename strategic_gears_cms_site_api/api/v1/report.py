import frappe
from strategic_gears_cms_site_api.utils import success_response, error_response,translate_keys

@frappe.whitelist(allow_guest=True)
def get_report_list(kwargs):
    try:
        user_language = kwargs.get('language')
        reports = frappe.get_all("Reports Master", fields=["label","name", "banner", "heading", "image","slug"])
        data_req = {
            "banner_data": {
                "banner_name": "",
            },
            "reports_list": []
        }

        banner_field = frappe.get_doc("Banner", reports[0].banner)
        data_req["banner_data"]["banner_name"] = banner_field.banner_name
        data_req["banner_data"]["banner_text"] = banner_field.banner_text
        data_req["banner_data"]["banner_background_image"] = banner_field.banner_background_image

        for report in reports:
            report_info = {
                "report_name": report.heading,
                "label":report.label,
                "report_image": report.image,
                "slug":report.slug
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
        user_language = kwargs.get('language')
        report_name = kwargs.get("name")
        reports = frappe.get_list("Reports Master", filters = {"slug":report_name},fields=['label','name','heading','description','attach_report','image'])
        for report in reports:
            if not report:
                return {"error": "Report not found"}

            report_detail = {
                "report_name": report.heading,
                "label":report.label,
                "report_image": report.image,
                "report_description": report.description,
                "report_file": report.attach_report,
                "other_reports": []
            }

        other_reports = frappe.get_all("Other Publications For Reports", filters={"parent": report.name}, fields=["other_publications"])

        for other_report in other_reports:
            other_report_doc = frappe.get_doc("Reports Master", other_report.other_publications)
            if other_report_doc:
                report_detail["other_reports"].append({
                    "report_name": other_report_doc.heading,
                    "label":other_report_doc.label,
                    "report_image": other_report_doc.image,
                    "slug":other_report_doc.slug
                })
        translated_data = translate_keys(report_detail, user_language)
        return success_response(data=translated_data)
    except Exception as e:
        frappe.logger("Report_list").exception(e)
        return error_response(e)
