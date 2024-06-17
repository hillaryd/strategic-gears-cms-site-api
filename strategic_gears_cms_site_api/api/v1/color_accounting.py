import frappe

from strategic_gears_cms_site_api.utils import error_response, success_response, translate_keys


@frappe.whitelist(allow_guest=True)
def get_color_accounting(kwargs):
	try:
		user_language = kwargs.get("language")
		color_accounting = frappe.get_doc("Color Accounting")
		banner_data = frappe.get_all(
			"Banner",
			filters={"banner_name": "COLOR ACCOUNTING LEARNING SYSTEM"},
			fields=[
				"banner_name",
				"banner_background_image",
				"banner_text_image",
				"banner_text",
				"banner_height",
				"banner_font_size",
				"banner_alignment",
			],
		)
		consultancy_heading = color_accounting.management_consultancy_heading
		consultancy_subheading = color_accounting.management_consultancy_subheading
		consultancy_description = color_accounting.management_consultancy_description
		background_heading = color_accounting.background_section_heading
		background_subheading = color_accounting.background_section_subheading
		background_description = color_accounting.background_section_description
		industries_data = frappe.get_all("Industry", fields=["industry_name"], order_by="sequence")
		industries_imgs = frappe.get_all(
			"Industry Images", fields=["industry_image"], order_by="sequence"
		)
		recognized_universities_description = color_accounting.recognized_universities_description
		recognized_universities_image = frappe.get_all(
			"Recognized Universities Images", fields=["university_image"]
		)
		learning_outcome_heading = color_accounting.learning_outcomes_heading
		learning_outcome_subheading = color_accounting.learning_outcomes_subheading
		learning_outcome_list = frappe.get_all("Learning Outcome", fields=["learning_outcome"])
		learning_outcome_image = color_accounting.learning_outcome_image
		highlited_background_section_description = (
			color_accounting.highlited_background_section_description
		)
		finacial_industry_description = color_accounting.finacial_industry_description
		consultancy_data = {
			"consultancy_heading": consultancy_heading,
			"consultancy_subheading": consultancy_subheading,
			"consultancy_description": consultancy_description,
		}
		background_data = {
			"background_heading": background_heading,
			"background_subheading": background_subheading,
			"background_description": background_description,
			"highlited_background_section_description": highlited_background_section_description,
			"finacial_industry_description": finacial_industry_description,
		}

		data = {
			"banner_data": banner_data[0],
			"consultancy_data": consultancy_data,
			"background_data": background_data,
			"industries_data": industries_data,
			"industries_image": industries_imgs,
			"recognized_universities_description": recognized_universities_description,
			"recognized_universities_image": recognized_universities_image,
			"learning_outcome_heading": learning_outcome_heading,
			"learning_outcome_subheading": learning_outcome_subheading,
			"learning_outcome_list": learning_outcome_list,
			"learning_outcome_image": learning_outcome_image,
		}
		translated_data = translate_keys(data, user_language)
		return success_response(data=translated_data)
	except Exception as e:
		frappe.logger("Color").exception(e)
		return error_response(e)
