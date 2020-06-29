from datetime import datetime
from sqlalchemy import create_engine, Column, Date, String
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from DataAnalyticsToolkit.config import *

"""
Mysql SQLAlchemy configuration
"""
mysql_engine = create_engine(f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_TABLE}')

mysql_db_session = scoped_session(sessionmaker(autocommit=False,
                                               autoflush=False,
                                               bind=mysql_engine))
MysqlBase = declarative_base()
MysqlBase.query = mysql_db_session.query_property()

mysql_connection = mysql_engine.connect()

"""
BigQuery SQLAlchemy configuration
"""
bq_engine = create_engine(f'bigquery://{BIG_QUERY_PROJECT}/{BIG_QUERY_DATA_SET}',
                          credentials_path=GOOGLE_APPLICATION_CREDENTIALS)

bq_db_session = scoped_session(sessionmaker(autocommit=False,
                                            autoflush=False,
                                            bind=bq_engine))
BigQueryBase = declarative_base()
BigQueryBase.query = bq_db_session.query_property()

bq_connection = bq_engine.connect()


class AuditedTable:
    """
    This class is a generic table with the audit fields used in all the audited tables.
    """

    create_date = Column(Date)
    update_date = Column(Date)
    create_user = Column(String)
    update_user = Column(String)

    def set_data(self, data):
        """Sets the basic audit data and call the specific data setter

        :param data: New object Dictionary
        :return: Validation error or error false
        """
        self.create_date = datetime.today().strftime('%Y-%m-%d')
        self.update_date = datetime.today().strftime('%Y-%m-%d')
        self.create_user = data["user"].email
        self.update_user = data["user"].email

        return self.set_module_specific_data(data)

    def set_module_specific_data(self, data):
        """To be overrated to set the specific module data

        :param data: New object Dictionary
        :return: Validation error or error false
        """
        raise NotImplementedError


def init_db():
    MysqlBase.metadata.create_all(bind=mysql_engine)
    BigQueryBase.metadata.create_all(bind=bq_engine)
