"""
This file contains redis operations
Author: Akshaya Revaskar
Date: 23/04/2020
"""

# importing required modules
import os
import redis
import logging

logging.basicConfig(level=logging.DEBUG)
from ..config.singleton import singleton
from ...users_env import Configuration
configuration = Configuration()
from ...settings import CACHE


@singleton
class RedisConnection:

    def __init__(self, **kwargs):
        self.connection = self.connect(**kwargs)

    def connect(self, **kwargs):
        connection = redis.StrictRedis(host=kwargs['host'],
                                       port=kwargs['port'],
                                       db=kwargs['db'])

        if connection:
            logging.info('Redis Cache Connection established')
        return connection

    # this function will set the dictionary into the redis to easily access
    def set(self, key, value, exp_s=None, exp_ms=None):
        self.connection.set(key, value, exp_s, exp_ms)
        logging.info(f'{key} : {value}')

    # this is the function for getting data from user
    def get(self, key):
        return self.connection.get(key)

    # checking if that particular key exists
    def exists(self, key):
        return self.connection.exists(key)

    # deleting the key which does not exist
    def delete(self, key):
        logging.info(f'Key to Delete : {key}')
        self.connection.delete(key)

    # disconnecting the redis connection
    def disconnect(self):
        self.connection.close()


redis_obj = RedisConnection(host=CACHE.get('redis_host'),
                            port=CACHE.get('redis_port'),
                            db=CACHE.get('redis_db'))
