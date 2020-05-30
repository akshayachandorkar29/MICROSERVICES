import json
from flask import Flask, request
from flasgger import Swagger, swag_from
from .settings import CONFIG
from nameko.standalone.rpc import ClusterRpcProxy
from werkzeug.wrappers import Response
from .auth.decorator import is_authenticated
from .common.utils import *

app = Flask(__name__)
Swagger(app)


@app.route('/register', methods=['POST'])
@swag_from('user_swagger.yml')
def register():
    request_data = json.loads(request.get_data(as_text=True))
    with ClusterRpcProxy(CONFIG) as rpc:  # using cluster rpc
        response = rpc.userService.registration_service(request_data)
        response = json.dumps(response)
    return Response(response=response, content_type='application/json', status=200)


@app.route('/activate/<string:token>', methods=['GET'])
@swag_from('user_swagger.yml')
def activate(**kwargs):
    request_data = {'token': kwargs.get('token')}
    with ClusterRpcProxy(CONFIG) as rpc:  # using cluster rpc
        response = rpc.userService.activate_registration_service(request_data)  # call the activation service
        response = json.dumps(response)
    return Response(response=response, content_type='application/json', status=200)


@app.route('/login', methods=['POST'])
@swag_from('user_swagger.yml')
def login():
    request_data = json.loads(request.get_data(as_text=True))
    with ClusterRpcProxy(CONFIG) as rpc:  # using cluster rpc
        response = rpc.userService.login_service(request_data)
        response = json.dumps(response)
    return Response(response=response, content_type='application/json', status=200)


@app.route('/forgot', methods=['POST'])
@swag_from('user_swagger.yml')
def forgot():
    request_data = json.loads(request.get_data(as_text=True))
    with ClusterRpcProxy(CONFIG) as rpc:  # using cluster rpc
        response = rpc.userService.forgot_service(request_data)  # call the forgot service
        response = json.dumps(response)
    return Response(response=response, content_type='application/json', status=200)


@app.route('/reset/<string:token>', methods=['PUT'])
@swag_from('user_swagger.yml')
def reset(**kwargs):
    request_data = json.loads(request.get_data(as_text=True))
    request_data['token'] = kwargs.get('token')
    with ClusterRpcProxy(CONFIG) as rpc:  # using cluster rpc
        response = rpc.userService.reset_password_service(request_data)  # call the reset service
        response = json.dumps(response)
    return Response(response=response, content_type='application/json', status=200)


@app.route('/create_note', methods=['POST'])
@swag_from('user_swagger.yml')
def create_note():
    request_data = json.loads(request.get_data(as_text=True))
    with ClusterRpcProxy(CONFIG) as rpc:  # using cluster rpc
        response = rpc.noteService.create_note_service(request_data)
        response = json.dumps(response)
    return Response(response=response, content_type='application/json', status=200)


@app.route('/create_label', methods=['POST'])
@swag_from('user_swagger.yml')
def create_label():
    request_data = json.loads(request.get_data(as_text=True))
    with ClusterRpcProxy(CONFIG) as rpc:  # using cluster rpc
        response = rpc.noteService.create_label_service(request_data)
        response = json.dumps(response)
    return Response(response=response, content_type='application/json', status=200)


if __name__ == '__main__':
    app.run(debug=True)
