"""
This is the utility file having frequently required functions
Author: Akshaya Revaskar
Date: 29-04-2020
"""
import json
import jwt
from sqlalchemy.ext.declarative import DeclarativeMeta
from ...users_env import Configuration
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


# class AlchemyEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj.__class__, DeclarativeMeta):
#             fields = {}
#             for field in [x for x in dir(obj) if not x.startswith('__') and x != 'metadata']:
#                 data = obj.__getattribute__(field)
#                 try:
#                     json.dumps(data)
#                     fields[field] = data
#                 except TypeError:
#                     fields[field] = None
#             return fields
#         return json.JSONEncoder.default(self, obj)


def serialize_data(coming_object):
    serializer_data = json.dumps(coming_object)
    data = json.loads(serializer_data)
    return data
