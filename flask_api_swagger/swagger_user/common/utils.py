"""
This is the utility file having frequently required functions
Author: Akshaya Revaskar
Date: 29-04-2020
"""

import json
import jwt
from sqlalchemy.ext.declarative import DeclarativeMeta
from ..swagger_env import Configuration
configuration = Configuration()


def create_jwt_token(id):
    try:
        payload = {'id': id}
        encoded_token = jwt.encode(payload, configuration.JWT_SECRET_KEY, algorithm='HS256').decode('utf-8')
    except:
        return None
    return encoded_token


def decode_jwt_token(token):
    try:
        decoded_token = jwt.decode(token, configuration.JWT_SECRET_KEY, algorithms=['HS256'])
    except:
        return None
    return decoded_token


def serialize_data(coming_object):
    serializer_data = json.dumps(coming_object)
    data = json.loads(serializer_data)
    return data

