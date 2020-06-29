import json
from datetime import datetime
from jinja2 import Environment
from sqlalchemy import Column, Date, String, Boolean, PrimaryKeyConstraint

from DataAnalyticsToolkit.database import AuditedTable, MysqlBase, mysql_db_session, bq_connection
from DataAnalyticsToolkit.commons import dry_run, get_datasets, upload_file


class QueryAutomation(MysqlBase, AuditedTable):
    __tablename__ = 'query_automation'

    data_source = Column(String)
    destination_dataset = Column(String)
    destination_table = Column(String)
    query_text = Column(String)
    date_field_name = Column(String)
    date_field_type = Column(String)
    date_field_format = Column(String)
    source_tables = Column(String)
    slack_contact = Column(String)
    owner = Column(String)
    comments = Column(String)
    start_date = Column(Date)
    active = Column(Boolean)

    __table_args__ = (
        PrimaryKeyConstraint("data_source", "destination_table", "active"),
        {}
    )

    def get(self):
        return self.query.filter(
            QueryAutomation.destination_dataset == self.destination_dataset,
            QueryAutomation.destination_table == self.destination_table,
            QueryAutomation.active.is_(True)
        ).first()

    def save(self):
        """Check if the test isn't already configured and save it to de database

        :return: Boolean. True if the configuration is saved correctly
        """
        check_test = self.query.filter(
            QueryAutomation.data_source == self.data_source,
            QueryAutomation.destination_table == self.destination_table,
            QueryAutomation.active.is_(True)
        ).first()
        if check_test is None:
            upload_result = self.upload_to_storage()
            if upload_result["error"]:
                return {"error": True, "message": upload_result["message"]}
            mysql_db_session.add(self)
            mysql_db_session.commit()
            return {"error": False}
        else:
            return {"error": True, "message": "The automation already exists"}

    def upload_to_storage(self):
        file_name = "config_query_automation_"
        file_name += f"{self.data_source}_{self.create_user}_{self.destination_dataset}_{self.destination_table}.json"

        json_config = json.dumps([{f["name"]: f["value"]} for f in self.fields])

        file = open(f"/tmp/{file_name}", "w")
        file.write(json_config)
        file.close()

        return upload_file("analytics-factory-query-automation", f"bigquery/{file_name}", f"/tmp/{file_name}")

    def set_module_specific_data(self, data):
        """Set the AB Testing configuration to the object

        :param data: Dict with configuration data to set
        :return: Dict with validation error or false
        """
        self.data_source = "BigQuery"
        self.source_tables = ','.join(data["source_tables"])
        self.slack_contact = data["slack_contact"]
        self.owner = data["user"].email
        self.comments = data["comments"]
        self.start_date = data["start_date"]
        self.active = "active" in data
        self.destination_dataset = data["destination_dataset"]
        self.destination_table = data["destination_table"]

        validation_result = self.validate_delete(
            data["destination_dataset"],
            data["destination_table"],
            data["date_field_name"],
            data["date_field_type"],
            data["date_field_format"]
        )
        if validation_result["error"]:
            validation_result["field"] = "Date Field Name, Type or Format"
            return validation_result
        self.date_field_name = data["date_field_name"]
        self.date_field_type = data["date_field_type"]
        self.date_field_format = data["date_field_format"]

        validation_result = self.validate_query(
            data["query_text"],
            data["date_field_name"],
            data["date_field_type"],
            data["date_field_format"]
        )
        if validation_result["error"]:
            validation_result["field"] = "query"
            return validation_result
        self.query_text = data["query_text"]

        return {"error": False}

    def validate_query(self, query_text, date_field_name, date_field_type, date_field_format):
        """Replace the `date` variable in the query string and performs a Dry_Run

        It uses the Jinja2 template formatting to parse query variables. Accepted Query variables:
        date_condition: it will be replaces with the date where condition

        :param query: String with the query to check
        :param date_field_name: String with the date field name
        :param date_field_type: String with the date field type
        :param date_field_format: String with the date field format
        :return: Dict with the check result
        """
        # TODO check if destination table is in the query
        # TODO check that the query string is only an insert
        date_condition = self.format_date_condition(date_field_name, date_field_type, date_field_format,
                                                    datetime.today())
        query_text = Environment().from_string(query_text).render(date_condition=date_condition)
        return dry_run(query=query_text)

    def validate_delete(self,
                        destination_dataset, destination_table, date_field_name, date_field_type, date_field_format):
        """Replace the `date_field` variable in the delete and performs a Dry_Run

        :param destination_dataset: String with the destination dataset name
        :param destination_table: String with the destination table name
        :param date_field_name: String with the date field name
        :param date_field_type: String with the date field type
        :param date_field_format: String with the date field format
        :return: Dict with the check result
        """
        date_condition = self.format_date_condition(date_field_name, date_field_type, date_field_format,
                                                    datetime.today())
        query = f"DELETE FROM `{destination_dataset}.{destination_table}` WHERE {date_condition}"
        return dry_run(query=query)

    def format_date_condition(self, date_field_name, date_field_type, date_field_format, date):
        """Formats the date condition based on the date field name, type and format and the required date

        :param date_field_name: String with the date field name
        :param date_field_type: String with the date field type
        :param date_field_format: String with the date field format
        :param date: Date Object, the required date
        :return: String, a sql valid condition
        """
        if date_field_type == "datetime" or date_field_type == "timestamp":
            date_field_name = f"DATE({date_field_name})"
        date_condition = f"{date_field_name} = '{date.strftime(date_field_format)}'"
        return date_condition

    def get_source_tables_options(self):
        """Get the available source tables from the Audit table

        :return: List, with the table names tuple
        """
        resource = bq_connection.execute("SELECT table FROM Audit.Uploaded_Data GROUP BY table")
        return [(row["table"], row["table"]) for row in resource]

    @property
    def id(self):
        return f"{self.destination_dataset}-{self.destination_table}"

    @property
    def path(self):
        return "query_automation"

    @staticmethod
    def module_actions(self):
        return []

    @property
    def fields(self):
        fields = []
        destination_dataset = {
            "label": "Destination Dataset",
            "name": "destination_dataset",
            "value": self.destination_dataset,
            "type": "select",
            "include_empty": True,
            "required": True,
            "is_parent": True,
            "child": "destination_table",
            "child_options_endpoint": "/query_automation/get_dataset_tables",
            "options": [(dataset, dataset) for dataset in sorted(get_datasets()) if dataset.startswith('user_')]
        }
        fields.append(destination_dataset)
        destination_table = {
            "label": "Destination Table",
            "name": "destination_table",
            "value": self.destination_table,
            "type": "select",
            "required": True,
            "include_empty": True,
            "options": []
        }
        fields.append(destination_table)
        source_tables = {
            "label": "Source Tables",
            "name": "source_tables",
            "value": self.source_tables,
            "type": "multiple",
            "required": True,
            "include_empty": True,
            "options": self.get_source_tables_options()
        }
        fields.append(source_tables)
        date_field_name = {
            "label": "Date Field Name",
            "name": "date_field_name",
            "value": self.date_field_name,
            "type": "text",
            "required": True
        }
        fields.append(date_field_name)
        date_field_type = {
            "label": "Date Field Type",
            "name": "date_field_type",
            "value": self.date_field_type,
            "type": "select",
            "required": True,
            "options": [("date", "DATE"), ("datetime", "DATETIME"), ("timestamp", "TIMESTAMP"), ("string", "STRING")]
        }
        fields.append(date_field_type)
        date_field_format = {
            "label": "Date Field Format",
            "name": "date_field_format",
            "value": self.date_field_format,
            "type": "text",
            "required": True
        }
        fields.append(date_field_format)
        slack_contact = {
            "label": "Slack User or Channel",
            "name": "slack_contact",
            "value": self.slack_contact,
            "type": "text",
            "required": True
        }
        fields.append(slack_contact)
        query_text = {
            "label": "Query",
            "name": "query_text",
            "value": self.query_text,
            "type": "textarea",
            "required": True
        }
        fields.append(query_text)
        comments = {
            "label": "Comments",
            "name": "comments",
            "value": self.comments,
            "type": "textarea",
            "required": False
        }
        fields.append(comments)
        start_date = {
            "label": "Start Date",
            "name": "start_date",
            "value": self.start_date,
            "type": "date",
            "required": True
        }
        fields.append(start_date)
        active = {
            "label": "Is Active",
            "name": "active",
            "value": self.active,
            "type": "checkbox",
            "required": False
        }
        fields.append(active)

        return fields

    def __repr__(self):
        return f'<QueryAutomation {self.destination_table}>'
