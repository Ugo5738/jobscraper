from datetime import datetime

from flask import redirect, url_for
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from wtforms import TextAreaField


# Admin classes
class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("auth.login"))


class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("auth.login"))


class PostAdminView(MyModelView):
    column_list = [
        "id",
        "website_name",
        "job_title",
        "job_company_name",
        "job_description",
        "location",
        "category",
        "salary_range",
        "post_time",
        "fill_date",
    ]
    column_searchable_list = ["website_name", "job_title", "job_company_name", "category"]
    column_filters = [
        "website_name",
        "job_title",
        "job_company_name",
        "location",
        "category",
        "salary_range",
        "post_time",
        "fill_date",
    ]
    form_columns = form_columns = [
        "website_name",
        "job_title",
        "job_company_name",
        "logo_url",
        "job_description",
        "location",
        "category",
        "salary_range",
        "post_time",
        "fill_date",
    ]

    form_args = {"job_description": {"label": "Job Description"}, "location": {"label": "Job Location"}}
    form_widget_args = {
        "job_description": {
            "rows": 10,
            "style": "max-height: 200px;",
            "widget": TextAreaField(),
        }
    }
    # column_default_sort = ("id", True)

    # override the on_form_prefill method to inject custom JS code to disable form submission on "Enter" key press
    def on_form_prefill(self, form, id):
        super(PostAdminView, self).on_form_prefill(form, id)
        form.job_description(class_="form-control")
        script = """
            <script>
            $(document).ready(function() {
                $('#job_description').keydown(function(event) {
                    if (event.keyCode == 13 && !event.shiftKey) {
                        event.preventDefault();
                    }
                });
            });
            </script>
        """
        self._template_args["custom_js"] = script

    def _job_description_formatter(view, context, model, name):
        return (
            model.job_description[:50] + "..." if len(model.job_description) > 50 else model.job_description
        )

    def _fill_date_formatter(view, context, model, name):
        fill_date_str = model.fill_date
        if isinstance(fill_date_str, str):
            fill_date = datetime.strptime(fill_date_str, "%Y-%m-%d")
        else:
            fill_date = fill_date_str
        return fill_date.strftime("%b %d, %Y %I:%M %p")

    column_formatters = {"job_description": _job_description_formatter, "fill_date": _fill_date_formatter}
