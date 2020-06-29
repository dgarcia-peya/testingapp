import json
from flask import request, make_response
from flask_login import login_required, current_user

from DataAnalyticsToolkit.views.dashboard import CreateView
from DataAnalyticsToolkit.commons import get_dataset_tables

from ...Query_Automation_Tool import query_automation_tool
from ..models.query_automation import QueryAutomation


class ToolCreateView(CreateView):

    @property
    def template_name(self):
        return 'query_automation_tool/create.html'

    @property
    def form(self):
        query_automation = QueryAutomation()
        form = {
            "id": "query_automation_form",
            "submit_function": "queryAutomationSubmit",
            "button": {"name": "query_automation_submit", "text": "Save"},
            "fields": query_automation.fields
        }
        return form


query_automation_tool.add_url_rule('/create', view_func=ToolCreateView.as_view('create_query_automation'))


@query_automation_tool.route("/save_query_automation", methods=['POST'])
@login_required
def save_test():
    """Save a new AB Test configuration

    :return: Json object
    """
    new_query_automation = request.get_json()
    new_query_automation["user"] = current_user

    query_automation = QueryAutomation()

    setting_result = query_automation.set_data(new_query_automation)
    if setting_result["error"]:
        return make_response({"error": setting_result["error"], "field": setting_result["field"]}, 400)

    saving_result = query_automation.save()
    if saving_result["error"]:
        return make_response({"error": saving_result["message"]}, 400)
    else:
        return make_response({"error": False}, 200)


@query_automation_tool.route("/get_dataset_tables")
@login_required
def get_tables():
    """Uses the BigQuery module to get the tables of a dataset

    :return: Json object with the table names
    """
    dataset_tables = get_dataset_tables(request.args.get('filter'))
    tables = [{"name": table, "value": table} for table in sorted(dataset_tables)]
    return json.dumps(tables)
