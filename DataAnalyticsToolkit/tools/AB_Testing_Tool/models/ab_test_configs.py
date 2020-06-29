from sqlalchemy import Column, Date, String, Boolean, sql

from DataAnalyticsToolkit.database import AuditedTable, MysqlBase, mysql_db_session
from DataAnalyticsToolkit.commons import dry_run, big_query_insert, big_query_execute_dml

from ..fwf_connector import get_projects
from ..config import *


class ABTestConfig(MysqlBase, AuditedTable):
    __tablename__ = 'ab_testing'

    ab_test_name = Column(String)
    fwf_project = Column(String)
    platform = Column(String)
    ab_test_short_description = Column(String)
    hypothesis = Column(String)
    tribe = Column(String)
    squad = Column(String)
    from_date = Column(Date)
    to_date = Column(Date)
    ab_test_location = Column(String)
    mcvr_standard = Column(String)
    mcvr_standard_description = Column(String)
    mcvr_custom = Column(String)
    mcvr_custom_descr = Column(String)
    custom_mcvr_is_shop = Column(Boolean)
    cvr_custom = Column(String)
    cvr_custom_descr = Column(String)
    mcvr_custom_additional = Column(String)
    mcvr_custom_additional_descr = Column(String)
    main_KPIs = Column(String)
    last_data_update_date = Column(Date)
    ab_test_control = Column(String)
    ab_test_variations = Column(String)
    ab_test_tags = Column(String)
    ab_test_result = Column(String)
    ab_test_explanation = Column(String)

    __mapper_args__ = {
        'primary_key': [ab_test_name]
    }

    def save(self):
        """Check if the test isn't already configured and save it to the database

        :return: Dictionary. Error false if the configuration is saved correctly in Mysql and BigQuery
        """
        check_test = self.query.get(self.ab_test_name)
        if check_test is None:
            big_query_error = self.save_to_big_query()
            if big_query_error["error"]:
                return {"error": True, "message": big_query_error["error"]}
            mysql_db_session.add(self)
            mysql_db_session.commit()
            return {"error": True, "message": "The AB Test configuration already exists"}
        else:
            return {"error": False}

    def save_to_big_query(self):
        """Use the BigQuery insert_rows functions to save the configuration in BigQuery

        :return: Dictionary with error False, exception error text, or BigQuery error object.
        """
        return big_query_insert(
            "bpy---pedidosya",
            "AB_Testing",
            "AB_Test_config",
            [
                (
                    self.platform,
                    self.ab_test_name,
                    self.ab_test_short_description,
                    self.hypothesis,
                    self.tribe,
                    self.squad,
                    self.from_date,
                    self.to_date,
                    self.ab_test_location,
                    self.mcvr_standard,
                    self.mcvr_standard_description,
                    self.mcvr_custom,
                    self.mcvr_custom_descr,
                    self.custom_mcvr_is_shop,
                    self.cvr_custom,
                    self.cvr_custom_descr,
                    self.mcvr_custom_additional,
                    self.mcvr_custom_additional_descr,
                    self.main_KPIs,
                    None,
                    self.last_data_update_date,
                    self.fwf_project,
                    self.create_date,
                    self.update_date,
                    self.create_user,
                    self.update_user,
                    self.ab_test_control,
                    self.ab_test_variations,
                    None,
                    None,
                    self.ab_test_tags,
                    None,
                    None,
                    None
                )
            ]
        )

    def set_module_specific_data(self, data):
        """Set the AB Testing configuration to the object

        :param data: Dict with configuration data to set
        :return: Void
        """
        self.ab_test_name = data["ab_test_name"]
        self.fwf_project = data["fwf_project"]
        self.platform = data["platform"]
        self.ab_test_short_description = data["short_description"]
        self.hypothesis = data["hypothesis"]
        self.tribe = data["tribe"]
        self.squad = data["squad"]
        self.from_date = data["from_date"]
        self.to_date = data["to_date"]
        self.ab_test_location = data["test_location"]
        self.ab_test_control = data["ab_test_control"]
        self.ab_test_variations = data["ab_test_variations"]
        self.mcvr_standard = data["mcvr_standard"]
        self.mcvr_standard_description = data["mcvr_standard_description"]
        self.ab_test_tags = data["ab_test_tags"]

        validation_result = self.validate_mcvr(data["mcvr_custom"])
        if validation_result["error"]:
            validation_result["field"] = "mcvr_custom"
            return validation_result
        self.mcvr_custom = data["mcvr_custom"]

        self.mcvr_custom_descr = data["mcvr_custom_descr"]
        self.custom_mcvr_is_shop = "custom_mcvr_is_shop" in data

        validation_result = self.validate_mcvr(data["cvr_custom"])
        if validation_result["error"]:
            validation_result["field"] = "cvr_custom"
            return validation_result
        self.cvr_custom = data["cvr_custom"]

        self.cvr_custom_descr = data["cvr_custom_descr"]

        if data["mcvr_custom_additional"] != "":
            validation_result = self.validate_mcvr(data["mcvr_custom_additional"])
            if validation_result["error"]:
                validation_result["field"] = "mcvr_custom_additional"
                return validation_result
        self.mcvr_custom_additional = data["mcvr_custom_additional"]

        self.mcvr_custom_additional_descr = data["mcvr_custom_additional_descr"]
        self.main_KPIs = data["main_kpi"]
        self.last_data_update_date = sql.null()

        return {"error": False}

    def validate_mcvr(self, condition):
        query = f"""SELECT
                fullVisitorId
                , visitId
                , date
                , platform
                , min(hitNumber) as min_hitNumber
                FROM `bpy---pedidosya.General_Tables.Pedidosya_ga_hits`
                WHERE date(date) = date_add(current_date(), interval -1 day)
                AND {condition} 
                GROUP BY 1,2,3,4"""
        return dry_run(query=query)

    def finish_test(self, ab_test_to_date, ab_test_result, ab_test_explanation):
        dml_statement = f"""
            UPDATE AB_Testing.AB_Test_config SET
            to_date="{ab_test_to_date}",
            ab_test_outcome="{ab_test_result}",
            ab_test_outcome_description="{ab_test_explanation}"
            WHERE ab_test_name="{self.ab_test_name}"
        """
        error = big_query_execute_dml(dml_statement)
        if error["error"]:
            return {"error": True, "message": error["error"]}

        self.to_date = ab_test_to_date
        self.ab_test_result = ab_test_result
        self.ab_test_explanation = ab_test_explanation
        mysql_db_session.commit()

        return {"error": False}

    @staticmethod
    def get(ab_test_name):
        ab_test = ABTestConfig.query.get(ab_test_name)
        return ab_test

    @property
    def id(self):
        return self.ab_test_name

    @property
    def path(self):
        return "ab_testing"

    @staticmethod
    def module_actions():
        actions = []
        finish_ab_test = {
            "label": "Finish AB Test Report",
            "function": "finishTest",
            "locations": "list"
        }
        actions.append(finish_ab_test)
        return actions

    @property
    def fields(self):
        fields = []
        fwf_project_field = {
            "label": "FWF Project",
            "name": "fwf_project",
            "value": self.fwf_project,
            "type": "select",
            "required": True,
            "include_empty": True,
            "is_parent": True,
            "child": "ab_test_name",
            "child_options_endpoint": "/ab_testing/get_fwf_property_names",
            "options": get_projects()
        }
        fields.append(fwf_project_field)
        ab_test_name = {
            "label": "AB Test Name",
            "name": "ab_test_name",
            "value": self.ab_test_name,
            "type": "select",
            "required": True,
            "include_empty": True,
            "on_change": "getFWFFeature",
            "options": []
        }
        fields.append(ab_test_name)
        short_description = {
            "label": "Short Description",
            "name": "short_description",
            "value": self.ab_test_short_description,
            "type": "textarea",
            "required": True
        }
        fields.append(short_description)
        hypothesis = {
            "label": "Hypothesis",
            "name": "hypothesis",
            "value": self.hypothesis,
            "type": "textarea",
            "required": True
        }
        fields.append(hypothesis)
        ab_test_tags = {
            "label": "AB Test Tags",
            "name": "ab_test_tags",
            "value": self.ab_test_tags,
            "type": "textarea",
            "required": True
        }
        fields.append(ab_test_tags)
        platform = {
            "label": "Platform",
            "name": "platform",
            "value": self.platform,
            "type": "select",
            "include_empty": True,
            "required": False,
            "options": [(platform, platform) for platform in sorted(PLATFORM_OPTIONS)]
        }
        fields.append(platform)
        tribe = {
            "label": "Tribe",
            "name": "tribe",
            "value": self.tribe,
            "type": "select",
            "include_empty": True,
            "required": True,
            "options": [(tribe, tribe) for tribe in TRIBE_OPTIONS]
        }
        fields.append(tribe)
        squad = {
            "label": "Squad",
            "name": "squad",
            "value": self.squad,
            "type": "select",
            "include_empty": True,
            "required": True,
            "options": [(squad, squad) for squad in SQUAD_OPTIONS]
        }
        fields.append(squad)
        from_date = {
            "label": "From Date",
            "name": "from_date",
            "value": self.from_date,
            "type": "date",
            "required": True
        }
        fields.append(from_date)
        to_date = {
            "label": "To Date",
            "name": "to_date",
            "value": self.to_date,
            "type": "date",
            "required": False
        }
        fields.append(to_date)
        ab_test_control = {
            "label": "AB Test Control",
            "name": "ab_test_control",
            "value": self.ab_test_control,
            "type": "text",
            "required": False,
            "read_only": True
        }
        fields.append(ab_test_control)
        ab_test_variations = {
            "label": "AB Test Variations",
            "name": "ab_test_variations",
            "value": self.ab_test_variations,
            "type": "textarea",
            "required": False,
            "read_only": True
        }
        fields.append(ab_test_variations)
        test_location = {
            "label": "Test Location",
            "name": "test_location",
            "value": self.ab_test_location,
            "type": "select",
            "include_empty": True,
            "required": True,
            "on_change": "setMcvrStandrad",
            "options": [(location["name"], location["name"]) for location in TEST_LOCATION_OPTIONS],
        }
        fields.append(test_location)
        mcvr_standard = {
            "label": "MCVR Standard",
            "name": "mcvr_standard",
            "value": self.mcvr_standard,
            "type": "textarea",
            "required": False,
            "read_only": True
        }
        fields.append(mcvr_standard)
        mcvr_standard_description = {
            "label": "MCVR Standard Description",
            "name": "mcvr_standard_description",
            "value": self.mcvr_standard_description,
            "type": "textarea",
            "required": True,
            "read_only": True
        }
        fields.append(mcvr_standard_description)
        mcvr_custom = {
            "label": "MCVR Custom",
            "name": "mcvr_custom",
            "value": self.mcvr_custom,
            "type": "textarea",
            "required": True
        }
        fields.append(mcvr_custom)
        mcvr_custom_description = {
            "label": "MCVR Custom Description",
            "name": "mcvr_custom_descr",
            "value": self.mcvr_custom_descr,
            "type": "textarea",
            "required": True
        }
        fields.append(mcvr_custom_description)
        custom_mcvr_is_shop = {
            "label": "MCVR Custom Is Shop",
            "name": "custom_mcvr_is_shop",
            "value": self.custom_mcvr_is_shop,
            "type": "checkbox",
            "required": False
        }
        fields.append(custom_mcvr_is_shop)
        cvr_custom = {
            "label": "CVR Custom",
            "name": "cvr_custom",
            "value": self.cvr_custom,
            "type": "textarea",
            "required": True
        }
        fields.append(cvr_custom)
        cvr_custom_description = {
            "label": "CVR Custom Description",
            "name": "cvr_custom_descr",
            "value": self.cvr_custom_descr,
            "type": "textarea",
            "required": True
        }
        fields.append(cvr_custom_description)
        mcvr_custom_additional = {
            "label": "MCVR Custom Additional",
            "name": "mcvr_custom_additional",
            "value": self.mcvr_custom_additional,
            "type": "textarea",
            "required": False
        }
        fields.append(mcvr_custom_additional)
        mcvr_custom_additional_description = {
            "label": "MCVR Custom Additional Description",
            "name": "mcvr_custom_additional_descr",
            "value": self.mcvr_custom_additional_descr,
            "type": "textarea",
            "required": False
        }
        fields.append(mcvr_custom_additional_description)
        main_kpi = {
            "label": "Main KPI",
            "name": "main_kpi",
            "value": self.main_KPIs,
            "type": "select",
            "include_empty": True,
            "required": True,
            "options": [(kpi, kpi) for kpi in sorted(MAIN_KPI_OPTIONS)]
        }
        fields.append(main_kpi)
        return fields

    def __repr__(self):
        return f'<AbTestConfig {self.ab_test_name}>'
