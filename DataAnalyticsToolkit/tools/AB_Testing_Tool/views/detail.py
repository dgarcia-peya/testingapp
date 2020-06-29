from flask import abort

from DataAnalyticsToolkit.views.dashboard import DetailView

from ...AB_Testing_Tool import ab_testing_tool
from ..models.ab_test_configs import ABTestConfig


class ToolDetailView(DetailView):

    @property
    def object(self):
        test_config = ABTestConfig.query.get(self.id)
        if test_config is not None:
            test_config.save_to_big_query()
            return test_config
        else:
            abort(404)


ab_testing_tool.add_url_rule('/detail/<id>', view_func=ToolDetailView.as_view('detail_ab_testing'))
