# import json
from flask import Flask, request
from flasgger import Swagger, swag_from
from .settings import CONFIG
from nameko.standalone.rpc import ClusterRpcProxy
from werkzeug.wrappers import Response
from .common.utils import *

app = Flask(__name__)
Swagger(app)


@app.route('/user/register', methods=['POST'])
@swag_from('swagger_user.yml')
def register():
    """
    This method is for user registration
    return: Response with response dictionary and status code
    """
    # converting request data from json to dictionary
    request_data = json.loads(request.get_data(as_text=True))
    with ClusterRpcProxy(CONFIG) as rpc:  # using cluster rpc
        response = rpc.userService.registration_service(request_data)
        # converting response from dictionary to json
        response = json.dumps(response)
    return Response(response=response, content_type='application/json', status=200)


@app.route('/user/activate/<string:token>', methods=['GET'])
@swag_from('swagger_user.yml')
def activate(**kwargs):
    """
    This method is for activating user
    :param kwargs: list of arguments with key
    :return: Response with response dictionary and status code
    """
    short_token = kwargs.get('token')
    with ClusterRpcProxy(CONFIG) as rpc:  # using cluster rpc
        response = rpc.userService.activate_registration_service(short_token)  # call the activation service
        # converting response from dictionary to json
        response = json.dumps(response)
    return Response(response=response, content_type='application/json', status=200)


@app.route('/user/login', methods=['POST'])
@swag_from('swagger_user.yml')
def login():
    """
    This method is user login method
    :return: Response with response dictionary and status code
    """
    # converting request data from json to dictionary
    request_data = json.loads(request.get_data(as_text=True))
    with ClusterRpcProxy(CONFIG) as rpc:  # using cluster rpc
        response = rpc.userService.login_service(request_data)
        # converting response from dictionary to json
        response = json.dumps(response)
    return Response(response=response, content_type='application/json', status=200)


@app.route('/user/forgot', methods=['POST'])
@swag_from('swagger_user.yml')
def forgot():
    """
    This method gets called if user forgets the password
    :return: Response with response dictionary and status code
    """
    # converting request data from json to dictionary
    request_data = json.loads(request.get_data(as_text=True))
    with ClusterRpcProxy(CONFIG) as rpc:  # using cluster rpc
        response = rpc.userService.forgot_service(request_data)  # call the forgot service
        # converting response from dictionary to json
        response = json.dumps(response)
    return Response(response=response, content_type='application/json', status=200)


@app.route('/user/reset/<string:token>', methods=['PUT'])
@swag_from('swagger_user.yml')
def reset(**kwargs):
    """
    This is the method for resetting user password
    :param kwargs: list of arguments with keys
    :return: Response with response dictionary and status code
    """
    # converting request data from json to dictionary
    request_data = json.loads(request.get_data(as_text=True))
    request_data['token'] = kwargs.get('token')
    with ClusterRpcProxy(CONFIG) as rpc:  # using cluster rpc
        response = rpc.userService.reset_password_service(request_data)  # call the reset service
        # converting response from dictionary to json
        response = json.dumps(response)
    return Response(response=response, content_type='application/json', status=200)


@app.route('/note/create', methods=['POST'])
@swag_from('note_swagger.yml')
def create():
    """
    This is the method for creating note
    :return: Response with response dictionary and status code
    """
    # converting request data from json to dictionary
    request_data = json.loads(request.get_data(as_text=True))
    token = request.headers['token']
    payload = decode_jwt_token(token)
    request_data['user_id'] = payload.get('id')
    with ClusterRpcProxy(CONFIG) as rpc:  # using cluster rpc
        response = rpc.noteService.create_note_service(request_data)
        # converting response from dictionary to json
        response = json.dumps(response)
    return Response(response=response, content_type='application/json', status=200)


@app.route('/note/read', methods=['GET'])
@swag_from('note_swagger.yml')
def read():
    """
    This is the method to read note
    :return: Response with response dictionary and status code
    """
    # retrieving token from read
    token = request.headers['token']
    payload = decode_jwt_token(token)
    request_data = {'user_id': payload.get('id')}
    with ClusterRpcProxy(CONFIG) as rpc:  # using cluster rpc
        response = rpc.noteService.read_note_service(request_data)
        # converting response from dictionary to json
        response = json.dumps(response)
    return Response(response=response, content_type='application/json', status=200)


@app.route('/note/update/<string:pk>', methods=['PUT'])
@swag_from('note_swagger.yml')
def update(**kwargs):
    """
    Method for updating note
    :param kwargs: list of arguments with keys
    :return: Response with response dictionary and status code
    """
    # converting request data from json to dictionary
    request_data = json.loads(request.get_data(as_text=True))
    # retrieving token from header
    token = request.headers['token']
    payload = decode_jwt_token(token)
    request_data['user_id'] = payload.get('id')
    request_data['id'] = kwargs.get('pk')
    with ClusterRpcProxy(CONFIG) as rpc:  # using cluster rpc
        response = rpc.noteService.update_note_service(request_data)  # call the reset service
        # converting response from dictionary to json
        response = json.dumps(response)
    return Response(response=response, content_type='application/json', status=200)


@app.route('/note/delete/<string:pk>', methods=['DELETE'])
@swag_from('note_swagger.yml')
def delete(**kwargs):
    """
    method for deleting note
    :param kwargs: list of arguments with keys
    :return: Response with response dictionary and status code
    """
    # retrieving token from header
    token = request.headers['token']
    payload = decode_jwt_token(token)
    request_data = dict()
    request_data['user_id'] = payload.get('id')
    request_data['id'] = kwargs.get('pk')
    with ClusterRpcProxy(CONFIG) as rpc:  # using cluster rpc
        response = rpc.noteService.delete_note_service(request_data)  # call the reset service
        # converting response from dictionary to json
        response = json.dumps(response)
    return Response(response=response, content_type='application/json', status=200)


@app.route('/note/pin/<string:pk>', methods=['PUT'])
@swag_from('note_swagger.yml')
def pin(**kwargs):
    """
    method for pin note
    :param kwargs: argumet list with keys
    :return: Response with response dictionary and status code
    """
    # converting request data from json to dictionary
    request_data = json.loads(request.get_data(as_text=True))
    token = request.headers['token']
    payload = decode_jwt_token(token)
    request_data['user_id'] = payload.get('id')
    request_data['id'] = kwargs.get('pk')
    with ClusterRpcProxy(CONFIG) as rpc:  # using cluster rpc
        response = rpc.noteService.pin_note_service(request_data)  # call the reset service
        # converting response from dictionary to json
        response = json.dumps(response)
    return Response(response=response, content_type='application/json', status=200)


@app.route('/note/archive/<string:pk>', methods=['PUT'])
@swag_from('note_swagger.yml')
def archive(**kwargs):
    """
    method for archive note
    :param kwargs: list of arguments with keys
    :return: Response with response dictionary nad status code
    """
    # converting request data from json to dictionary
    request_data = json.loads(request.get_data(as_text=True))
    token = request.headers['token']
    payload = decode_jwt_token(token)
    request_data['user_id'] = payload.get('id')
    request_data['id'] = kwargs.get('pk')
    with ClusterRpcProxy(CONFIG) as rpc:  # using cluster rpc
        response = rpc.noteService.archive_note_service(request_data)  # call the reset service
        # converting response from dictionary to json
        response = json.dumps(response)
    return Response(response=response, content_type='application/json', status=200)


@app.route('/note/restore/<string:pk>', methods=['PUT'])
@swag_from('note_swagger.yml')
def restore(**kwargs):
    """
    method for restoring note
    :param kwargs: list of arguments with keys
    :return: Response with response dictionary and status code
    """
    # converting request data from json to dictionary
    request_data = json.loads(request.get_data(as_text=True))
    token = request.headers['token']
    payload = decode_jwt_token(token)
    request_data['user_id'] = payload.get('id')
    request_data['id'] = kwargs.get('pk')
    with ClusterRpcProxy(CONFIG) as rpc:  # using cluster rpc
        response = rpc.noteService.restore_note_service(request_data)  # call the reset service
        # converting response from dictionary to json
        response = json.dumps(response)
    return Response(response=response, content_type='application/json', status=200)


@app.route('/label/create', methods=['POST'])
@swag_from('label_swagger.yml')
def label_create():
    """
    method for creating label
    :return: Response with response dictionary and status code
    """
    # converting request data from json to dictionary
    request_data = json.loads(request.get_data(as_text=True))
    token = request.headers['token']
    payload = decode_jwt_token(token)
    request_data['user_id'] = payload.get('id')
    with ClusterRpcProxy(CONFIG) as rpc:  # using cluster rpc
        response = rpc.noteService.create_label_service(request_data)
        # converting response from dictionary to json
        response = json.dumps(response)
    return Response(response=response, content_type='application/json', status=200)


@app.route('/label/read', methods=['GET'])
@swag_from('label_swagger.yml')
def label_read():
    """
    this is the method for reading label
    :return: Response with response dictionary and status code
    """
    # retrieving token from header
    token = request.headers['token']
    payload = decode_jwt_token(token)
    request_data = {'user_id': payload.get('id')}
    with ClusterRpcProxy(CONFIG) as rpc:  # using cluster rpc
        response = rpc.noteService.read_label_service(request_data)
        # converting response from dictionary to json
        response = json.dumps(response)
    return Response(response=response, content_type='application/json', status=200)


@app.route('/label/update/<string:pk>', methods=['PUT'])
@swag_from('label_swagger.yml')
def label_update(**kwargs):
    """
    This method is for updating label
    :param kwargs: list of arguments with keys
    :return: Response with response dictionary and status code
    """
    # converting request data from json to dictionary
    request_data = json.loads(request.get_data(as_text=True))
    token = request.headers['token']
    payload = decode_jwt_token(token)
    request_data['user_id'] = payload.get('id')
    request_data['id'] = kwargs.get('pk')
    with ClusterRpcProxy(CONFIG) as rpc:  # using cluster rpc
        response = rpc.noteService.update_label_service(request_data)  # call the reset service
        # converting response from dictionary to json
        response = json.dumps(response)
    return Response(response=response, content_type='application/json', status=200)


@app.route('/label/delete/<string:pk>', methods=['DELETE'])
@swag_from('label_swagger.yml')
def label_delete(**kwargs):
    """
    this is the method for deleting label
    :param kwargs: list of arguments with keys
    :return: Response with response dictionary and status code
    """
    # retrieving token from header
    token = request.headers['token']
    payload = decode_jwt_token(token)
    request_data = dict()
    request_data['user_id'] = payload.get('id')
    request_data['id'] = kwargs.get('pk')
    with ClusterRpcProxy(CONFIG) as rpc:  # using cluster rpc
        response = rpc.noteService.delete_label_service(request_data)  # call the reset service
        # converting response from dictionary to json
        response = json.dumps(response)
    return Response(response=response, content_type='application/json', status=200)


if __name__ == '__main__':
    app.run(debug=True)
