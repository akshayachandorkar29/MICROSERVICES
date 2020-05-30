"""
This is the utility file having frequently required functions
Author: Akshaya Revaskar
Date: 29-04-2020
"""
# importing necessary modules
import json
import jwt
from ...notes_env import Configuration
configuration = Configuration()


# method for creating token with jwt
def create_jwt_token(id):
    try:
        # setting the payload
        payload = {'id': id}
        encoded_token = jwt.encode(payload, configuration.JWT_SECRET_KEY, algorithm='HS256').decode('utf-8')
    except:
        return None
    return encoded_token


# method for decoding token
def decode_jwt_token(token):
    try:
        decoded_token = jwt.decode(token, configuration.JWT_SECRET_KEY, algorithms=['HS256'])
    except:
        return None
    return decoded_token


def serialize_data(object):
    serializer_data = json.dumps(object)
    data = json.loads(serializer_data)
    return data
