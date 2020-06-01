"""
This file contains settings for user service
"""
from .notes_env import Configuration
configuration = Configuration()

CACHE = {
    'host': configuration.MICRO_REDIS_HOST,
    'port': configuration.MICRO_REDIS_PORT,
    'db': configuration.MICRO_REDIS_DB
}

MYSQL_DB_CONFIG = {
    'user': configuration.MICRO_DB_USER,
    'password': configuration.MICRO_DB_PASSWORD,
    'host': configuration.MICRO_DB_HOST,
    'port': configuration.MICRO_DB_PORT,
    'db_name': configuration.MICRO_DB_NAME
}
