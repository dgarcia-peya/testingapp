from flask import abort

from DataAnalyticsToolkit.views.dashboard import DetailView

from ...Query_Automation_Tool import query_automation_tool
from ..models.query_automation import QueryAutomation


class ToolDetailView(DetailView):

    @property
    def object(self):
        query_automation = QueryAutomation()
        query_automation.destination_dataset = self.id.split("-")[0]
        query_automation.destination_table = self.id.split("-")[1]
        query_automation = query_automation.get()
        if query_automation is not None:
            return query_automation
        else:
            abort(404)


query_automation_tool.add_url_rule('/detail/<id>', view_func=ToolDetailView.as_view('detail_query_automation'))
