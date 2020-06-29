import json
from flask import request, make_response
from flask_login import login_required, current_user

from DataAnalyticsToolkit.views.dashboard import CreateView

from ...AB_Testing_Tool import ab_testing_tool
from ..models.ab_test_configs import ABTestConfig
from ..config import *
from ..fwf_connector import get_features_list, get_feature_data


class ToolCreateView(CreateView):

    @property
    def template_name(self):
        return 'ab_testing_tool/create.html'

    @property
    def form(self):
        test_config = ABTestConfig()
        form = {
            "id": "ab_testing_form",
            "submit_function": "abTestingSubmit",
            "button": {"name": "ab_testing_submit", "text": "Save"},
            "fields": test_config.fields
        }
        return form


ab_testing_tool.add_url_rule('/create', view_func=ToolCreateView.as_view('create_ab_testing'))


@ab_testing_tool.route("/save_ab_test", methods=['POST'])
@login_required
def save_test():
    """Save a new AB Test configuration

    :return: Json object
    """
    new_config = request.get_json()
    new_config["user"] = current_user

    ab_test = ABTestConfig()

    setting_result = ab_test.set_data(new_config)
    if setting_result["error"]:
        return make_response({"error": setting_result["error"], "field": setting_result["field"]}, 400)

    saving_result = ab_test.save()
    if saving_result["error"]:
        return make_response({"error": saving_result["message"]}, 400)
    else:
        return make_response({"error": False}, 200)


@ab_testing_tool.route("/get_fwf_property_names")
@login_required
def get_fwf_property_names():
    """consume the FWF API to get the AB Test names from a project

    :return: Json object with the Test names
    """
    properties = []
    fwf_properties = get_features_list(request.args.get('filter'))
    for fwf_property in fwf_properties["result"]:
        if fwf_property["kind"] == "abntest":
            flag = {
                "name": fwf_property["key"],
                "value": fwf_property["key"]
            }
            properties.append(flag)
    return json.dumps(properties)


@ab_testing_tool.route("/get_fwf_property_config")
@login_required
def get_fwf_property_config():
    """Consume the FWF API to get an AB Test data

    :return: Json Object with the test DATA
    """
    fwf_configurations = get_feature_data(request.args.get('project'), request.args.get('property'))
    return json.dumps(fwf_configurations)


@ab_testing_tool.route("/get_mcvr_standard")
@login_required
def get_mcvr_standard():
    """Gets the mvcr_standard and mvcr_standard_description from configuration

    :return: Json Object with the mvcr_standard data
    """
    mvcr_standard = [item for item in TEST_LOCATION_OPTIONS if item["name"] == request.args.get('test_location')][0]
    return json.dumps(mvcr_standard)
