"""
This file contains settings for user service
"""
from .users_env import Configuration
configuration = Configuration()

JWT_SECRET_KEY = configuration.JWT_SECRET_KEY

CACHE = {
    'redis_host': configuration.MICRO_REDIS_HOST,
    'redis_port': configuration.MICRO_REDIS_PORT,
    'redis_db': configuration.MICRO_REDIS_DB
}

MYSQL_DB_CONFIG = {
    'user': configuration.MICRO_DB_USER,
    'password': configuration.MICRO_DB_PASSWORD,
    'host': configuration.MICRO_DB_HOST,
    'port': configuration.MICRO_DB_PORT,
    'db_name': configuration.MICRO_DB_NAME
}

EMAIL_FROM = configuration.MICRO_EMAIL_FROM
EMAIL_PASSWORD = configuration.MICRO_EMAIL_PASSWORD

HOST = configuration.MICRO_HOST
PORT = configuration.MICRO_PORT
