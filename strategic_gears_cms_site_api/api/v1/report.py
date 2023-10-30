import frappe
from strategic_gears_cms_site_api.utils import success_response, error_response

@frappe.whitelist(allow_guest=True)
def get_report_list(kwargs):
    try:
        reports = frappe.get_all("Reports Master", fields=["name", "banner", "heading", "image","slug"])
        data_req = {
            "banner_data": {
                "banner_name": "",
            },
            "reports_list": []
        }

        banner_field = frappe.get_doc("Banner", reports[0].banner)
        data_req["banner_data"]["banner_name"] = banner_field.banner_name
        data_req["banner_data"]["banner_text_image"] = banner_field.banner_text_image
        data_req["banner_data"]["banner_background_image"] = banner_field.banner_background_image

        for report in reports:
            report_info = {
                "report_name": report.heading,
                "report_image": report.image,
                "slug":report.slug
            }
            data_req["reports_list"].append(report_info)

        return success_response(data=data_req)
    except Exception as e:
        frappe.logger("Report_list").exception(e)
        return error_response(e)

@frappe.whitelist(allow_guest=True)
def report_details(kwargs):
    try:
        report_name = kwargs.get("name")
        reports = frappe.get_list("Reports Master", filters = {"slug":report_name},fields=['name','heading','description','attach_report','image'])
        for report in reports:
            if not report:
                return {"error": "Report not found"}

            report_detail = {
                "report_name": report.heading,
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
                    "report_image": other_report_doc.image,
                    "slug":other_report_doc.slug
                })

        return success_response(data=report_detail)
    except Exception as e:
        frappe.logger("Report_list").exception(e)
        return error_response(e)
