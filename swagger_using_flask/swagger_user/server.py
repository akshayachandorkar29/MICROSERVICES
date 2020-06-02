# import json
from flask import Flask, request
from flasgger import Swagger, swag_from
from .settings import CONFIG
from nameko.standalone.rpc import ClusterRpcProxy
from werkzeug.wrappers import Response
from .common.utils import *

app = Flask(__name__)
Swagger(app)


@app.route('/user_register', methods=['POST'])
@swag_from('swagger_user.yml')
def register():
    request_data = json.loads(request.get_data(as_text=True))
    with ClusterRpcProxy(CONFIG) as rpc:  # using cluster rpc
        response = rpc.userService.registration_service(request_data)
        response = json.dumps(response)
    return Response(response=response, content_type='application/json', status=200)


@app.route('/activate_user/<string:token>', methods=['GET'])
@swag_from('swagger_user.yml')
def activate(**kwargs):
    request_data = {'token': kwargs.get('token')}
    with ClusterRpcProxy(CONFIG) as rpc:  # using cluster rpc
        response = rpc.userService.activate_registration_service(request_data)  # call the activation service
        response = json.dumps(response)
    return Response(response=response, content_type='application/json', status=200)


@app.route('/user_login', methods=['POST'])
@swag_from('swagger_user.yml')
def login():
    request_data = json.loads(request.get_data(as_text=True))
    with ClusterRpcProxy(CONFIG) as rpc:  # using cluster rpc
        response = rpc.userService.login_service(request_data)
        response = json.dumps(response)
    return Response(response=response, content_type='application/json', status=200)


@app.route('/forgot_password', methods=['POST'])
@swag_from('swagger_user.yml')
def forgot():
    request_data = json.loads(request.get_data(as_text=True))
    with ClusterRpcProxy(CONFIG) as rpc:  # using cluster rpc
        response = rpc.userService.forgot_service(request_data)  # call the forgot service
        response = json.dumps(response)
    return Response(response=response, content_type='application/json', status=200)


@app.route('/reset_password/<string:token>', methods=['PUT'])
@swag_from('swagger_user.yml')
def reset(**kwargs):
    request_data = json.loads(request.get_data(as_text=True))
    request_data['token'] = kwargs.get('token')
    with ClusterRpcProxy(CONFIG) as rpc:  # using cluster rpc
        response = rpc.userService.reset_password_service(request_data)  # call the reset service
        response = json.dumps(response)
    return Response(response=response, content_type='application/json', status=200)


@app.route('/create_note', methods=['POST'])
@swag_from('note_swagger.yml')
def create():
    request_data = json.loads(request.get_data(as_text=True))
    with ClusterRpcProxy(CONFIG) as rpc:  # using cluster rpc
        response = rpc.noteService.create_note_service(request_data)
        response = json.dumps(response)
    return Response(response=response, content_type='application/json', status=200)


@app.route('/read_note/<string:pk>', methods=['GET'])
@swag_from('note_swagger.yml')
def read(**kwargs):
    request_data = {'id': kwargs.get('pk')}
    with ClusterRpcProxy(CONFIG) as rpc:  # using cluster rpc
        response = rpc.noteService.read_note_service(request_data)
        response = json.dumps(response)
    return Response(response=response, content_type='application/json', status=200)


@app.route('/update_note/<string:pk>', methods=['PUT'])
@swag_from('note_swagger.yml')
def update(**kwargs):
    request_data = json.loads(request.get_data(as_text=True))
    request_data['id'] = kwargs.get('pk')
    with ClusterRpcProxy(CONFIG) as rpc:  # using cluster rpc
        response = rpc.noteService.update_note_service(request_data)  # call the reset service
        response = json.dumps(response)
    return Response(response=response, content_type='application/json', status=200)


@app.route('/delete_note/<string:pk>', methods=['DELETE'])
@swag_from('note_swagger.yml')
def delete(**kwargs):
    request_data = {'id': kwargs.get('pk')}
    with ClusterRpcProxy(CONFIG) as rpc:  # using cluster rpc
        response = rpc.noteService.delete_note_service(request_data)  # call the reset service
        response = json.dumps(response)
    return Response(response=response, content_type='application/json', status=200)


@app.route('/create_label', methods=['POST'])
@swag_from('label_swagger.yml')
def label_create():
    request_data = json.loads(request.get_data(as_text=True))
    with ClusterRpcProxy(CONFIG) as rpc:  # using cluster rpc
        response = rpc.noteService.create_label_service(request_data)
        response = json.dumps(response)
    return Response(response=response, content_type='application/json', status=200)


@app.route('/read_label/<string:pk>', methods=['GET'])
@swag_from('label_swagger.yml')
def label_read(**kwargs):
    request_data = {'id': kwargs.get('pk')}
    with ClusterRpcProxy(CONFIG) as rpc:  # using cluster rpc
        response = rpc.noteService.read_label_service(request_data)
        response = json.dumps(response)
    return Response(response=response, content_type='application/json', status=200)


@app.route('/update_label/<string:pk>', methods=['PUT'])
@swag_from('label_swagger.yml')
def label_update(**kwargs):
    request_data = json.loads(request.get_data(as_text=True))
    request_data['id'] = kwargs.get('pk')
    with ClusterRpcProxy(CONFIG) as rpc:  # using cluster rpc
        response = rpc.noteService.update_label_service(request_data)  # call the reset service
        response = json.dumps(response)
    return Response(response=response, content_type='application/json', status=200)


@app.route('/delete_label/<string:pk>', methods=['DELETE'])
@swag_from('label_swagger.yml')
def label_delete(**kwargs):
    request_data = {'id': kwargs.get('pk')}
    with ClusterRpcProxy(CONFIG) as rpc:  # using cluster rpc
        response = rpc.noteService.delete_label_service(request_data)  # call the reset service
        response = json.dumps(response)
    return Response(response=response, content_type='application/json', status=200)


if __name__ == '__main__':
    app.run(debug=True)
