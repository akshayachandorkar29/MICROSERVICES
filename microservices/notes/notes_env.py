"""
This is the environment file
Author: Akshaya Revaskar
"""


class Configuration:
    JWT_SECRET_KEY = 'secret'
    MICRO_REDIS_HOST = "localhost"
    MICRO_REDIS_PORT = "6379"
    MICRO_REDIS_DB = "0"

    MICRO_DB_NAME = "micro_db"
    MICRO_DB_PORT = "3306"
    MICRO_DB_HOST = "localhost"
    MICRO_DB_USER = "root"
    MICRO_DB_PASSWORD = "password"
