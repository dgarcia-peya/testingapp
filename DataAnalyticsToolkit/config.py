import os

"""Configuration File

Main app configuration set
The values are read from the environment or take a default one
"""

"""Secret key to encrypt sessions cookies"""
APP_SECRET_KEY = os.environ.get("SECRET_KEY", os.urandom(24))

"""Google Auth configuration"""
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = os.environ.get("GOOGLE_DISCOVERY_URL", None)
SUPPORTED_LOGIN_DOMAINS = ["pedidosya.com"]

"""Google Cloud Credentials"""
GOOGLE_APPLICATION_CREDENTIALS = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", None)

"""BigQuery parameters"""
BIG_QUERY_PROJECT = os.environ.get("BIG_QUERY_PROJECT", None)
BIG_QUERY_DATA_SET = os.environ.get("BIG_QUERY_DATA_SET", None)

"""Mysql configuration"""
MYSQL_USER = os.environ.get("MYSQL_USER", None)
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", None)
MYSQL_HOST = os.environ.get("MYSQL_HOST", None)
MYSQL_TABLE = os.environ.get("MYSQL_TABLE", None)
