from DataAnalyticsToolkit.views.dashboard import ListView
from ...AB_Testing_Tool import ab_testing_tool
from ..models.ab_test_configs import ABTestConfig
from DataAnalyticsToolkit.database import mysql_db_session


class ToolListView(ListView):

    @property
    def template_name(self):
        return 'ab_testing_tool/list.html'

    @property
    def actions(self):
        return [a for a in ABTestConfig.module_actions() if "list" in a["locations"]]

    @property
    def objects(self):
        db_objects = mysql_db_session.query(
            ABTestConfig.ab_test_name,
            ABTestConfig.fwf_project,
            ABTestConfig.platform,
            ABTestConfig.ab_test_short_description,
            ABTestConfig.ab_test_tags,
            ABTestConfig.hypothesis,
            ABTestConfig.tribe,
            ABTestConfig.squad,
            ABTestConfig.from_date,
            ABTestConfig.to_date,
            ABTestConfig.ab_test_location,
            ABTestConfig.mcvr_standard,
            ABTestConfig.mcvr_standard_description,
            ABTestConfig.mcvr_custom,
            ABTestConfig.mcvr_custom_descr,
            ABTestConfig.custom_mcvr_is_shop,
            ABTestConfig.cvr_custom,
            ABTestConfig.cvr_custom_descr,
            ABTestConfig.mcvr_custom_additional,
            ABTestConfig.mcvr_custom_additional_descr,
            ABTestConfig.main_KPIs,
            ABTestConfig.last_data_update_date
        )
        dict_objects = []
        for db_object in db_objects:
            dict_object = db_object._asdict()
            # _asdict method name starts with an underscore, to match the namedtuple API (it's not private!)
            dict_object["path"] = "ab_testing"
            dict_object["id"] = db_object.ab_test_name
            dict_objects.append(dict_object)
        return dict_objects


ab_testing_tool.add_url_rule('/list', view_func=ToolListView.as_view('list_ab_testing'))
