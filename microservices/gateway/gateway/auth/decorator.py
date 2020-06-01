"""
This file has decorator method
Author: Akshaya Revaskar
Date: 29-04-2020
"""

# importing neccessary modules and packages
from ..common.utils import *
from ..config.redis_connection import RedisConnection
redis_obj = RedisConnection()


def is_authenticated(method):
    def authenticate_user(self, request, **kwargs):
        """
        This is the decorator method
        :param request: request coming from client to server
        :param kwargs: arguments with keys
        :return: method authenticate_user
        """
        try:
            print(request.path, type(request.path))
            if request.path not in ['/forgot', '/register', '/login']:
                token = request.headers['token']
                payload = decode_jwt_token(token)
                id_key = payload['id']
                token = redis_obj.get(id_key)

                if token is None:
                    raise ValueError('You need to login first')
                return method(self, request, **kwargs)
            else:
                return method(self, request, **kwargs)
        except jwt.ExpiredSignatureError:
            raise Exception("Signature Expired. Please Log In Again...")
        except jwt.DecodeError:
            raise Exception("Decode Error")
    return authenticate_user
