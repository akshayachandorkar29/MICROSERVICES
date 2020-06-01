"""
This is the utility file having frequently required functions
Author: Akshaya Revaskar
Date: 29-04-2020
"""

import jwt
from ...gateway_env import Configuration
configuration = Configuration()


# function for creating jwt token
def create_jwt_token(id):
    """
    method to create jwt token
    :param id: user id to create payload
    :return: encoded token with user id
    """
    try:
        payload = {'id': id}  # setting the payload
        encoded_token = jwt.encode(payload, configuration.JWT_SECRET_KEY, algorithm='HS256').decode('utf-8')
    except:
        return None
    return encoded_token


# function for decoding token
def decode_jwt_token(token):
    """
    method to decode token
    :param token: token received from user to decode
    :return: decoded token
    """
    try:
        decoded_token = jwt.decode(token, configuration.JWT_SECRET_KEY, algorithms=['HS256'])
    except:
        return None
    return decoded_token
