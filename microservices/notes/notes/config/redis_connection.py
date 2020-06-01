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
from ...notes_env import Configuration
configuration = Configuration()


@singleton
class RedisConnection:
    """
    class for connecting redis
    """

    def __init__(self, **kwargs):
        self.connection = self.connect(**kwargs)

    def connect(self, **kwargs):
        """
        method for connecting redis
        :param kwargs: arguments with keys
        :return: connection
        """
        connection = redis.StrictRedis(host=kwargs['host'],
                                       port=kwargs['port'],
                                       db=kwargs['db'])

        if connection:
            logging.info('Redis Cache Connection established')
        return connection

    # this function will set the dictionary into the redis to easily access
    def set(self, key, value, exp_s=None, exp_ms=None):
        """
        method for setting key in redis
        :param key: key to set
        :param value: value for key
        :param exp_s: expiry time in seconds
        :param exp_ms: expiry time in miliseconds
        """
        self.connection.set(key, value, exp_s, exp_ms)
        logging.info(f'{key} : {value}')

    # this is the function for getting data from user
    def get(self, key):
        """
        method for getting value from redis
        :param key: key to get data
        :return: key
        """
        return self.connection.get(key)

    # checking if that particular key exists
    def exists(self, key):
        """
        method to check the key exists
        :param key: key to check if it exist
        :return: key
        """
        return self.connection.exists(key)

    # deleting the key which does not exist
    def delete(self, key):
        """
        method to delete key from redis
        :param key: key to delete
        :return: key
        """
        logging.info(f'Key to Delete : {key}')
        self.connection.delete(key)

    # disconnecting the redis connection
    def disconnect(self):
        """
        method to disconnect redis
        """
        self.connection.close()


redis_obj = RedisConnection(host=configuration.MICRO_REDIS_HOST,
                            port=configuration.MICRO_REDIS_PORT,
                            db=configuration.MICRO_REDIS_DB)
