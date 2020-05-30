"""
This file has decorator
Author: Akshaya Revaskar
Date: 29-04-2020
"""

# importing neccessary modules and packages
import jwt
from ..common.utils import decode_jwt_token
from ..config.redis_connection import RedisConnection
redis_obj = RedisConnection()


def is_authenticated(method):
    def authenticate_user(self, request, **kwargs):
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
