from DataAnalyticsToolkit.views.dashboard import ListView
from DataAnalyticsToolkit.database import mysql_db_session
from ...Query_Automation_Tool import query_automation_tool
from ..models.query_automation import QueryAutomation


class ToolListView(ListView):

    @property
    def objects(self):
        db_objects = mysql_db_session.query(QueryAutomation.data_source,
                                            QueryAutomation.destination_dataset,
                                            QueryAutomation.destination_table,
                                            QueryAutomation.query_text,
                                            QueryAutomation.date_field_name,
                                            QueryAutomation.date_field_type,
                                            QueryAutomation.date_field_format,
                                            QueryAutomation.source_tables,
                                            QueryAutomation.slack_contact,
                                            QueryAutomation.owner,
                                            QueryAutomation.comments,
                                            QueryAutomation.start_date,
                                            QueryAutomation.active)
        dict_objects = []
        for db_object in db_objects:
            dict_object = db_object._asdict()
            # _asdict method name starts with an underscore, to match the namedtuple API (it's not private!)
            dict_object["path"] = "query_automation"
            dict_object["id"] = f"{db_object.destination_dataset}-{db_object.destination_table}"
            dict_objects.append(dict_object)
        return dict_objects


query_automation_tool.add_url_rule('/list', view_func=ToolListView.as_view('list_query_automation'))
