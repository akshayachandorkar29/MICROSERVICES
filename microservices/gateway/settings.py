"""
This file contains settings for user service
"""
from .gateway_env import Configuration
configuration = Configuration()

CACHE = {
    'host': configuration.MICRO_REDIS_HOST,
    'port': configuration.MICRO_REDIS_PORT,
    'db': configuration.MICRO_REDIS_DB
}
