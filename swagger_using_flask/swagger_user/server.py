import json
from flask import Flask, request
from flasgger import Swagger, swag_from
from .settings import CONFIG
from nameko.standalone.rpc import ClusterRpcProxy
from werkzeug.wrappers import Response
from .common.utils import *

app = Flask(__name__)
app.config["SWAGGER"] = {"title": "Swagger_Microservices", "uiversion": 2}

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec_1",
            "route": "/apispec_1.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/swagger/",
}

swagger = Swagger(app, config=swagger_config)


@app.route('/register', methods=['POST'])
@swag_from('new_user_swagger.yml')
def register():
    request_data = json.loads(request.get_data(as_text=True))
    with ClusterRpcProxy(CONFIG) as rpc:  # using cluster rpc
        response = rpc.userService.registration_service(request_data)
        response = json.dumps(response)
    return Response(response=response, content_type='application/json', status=200)


@app.route('/activate/<string:token>', methods=['GET'])
@swag_from('new_user_swagger.yml')
def activate(**kwargs):
    request_data = {'token': kwargs.get('token')}
    with ClusterRpcProxy(CONFIG) as rpc:  # using cluster rpc
        response = rpc.userService.activate_registration_service(request_data)  # call the activation service
        response = json.dumps(response)
    return Response(response=response, content_type='application/json', status=200)


@app.route('/login', methods=['POST'])
@swag_from('new_user_swagger.yml')
def login():
    request_data = json.loads(request.get_data(as_text=True))
    with ClusterRpcProxy(CONFIG) as rpc:  # using cluster rpc
        response = rpc.userService.login_service(request_data)
        response = json.dumps(response)
    return Response(response=response, content_type='application/json', status=200)


@app.route('/forgot', methods=['POST'])
@swag_from('new_user_swagger.yml')
def forgot():
    request_data = json.loads(request.get_data(as_text=True))
    with ClusterRpcProxy(CONFIG) as rpc:  # using cluster rpc
        response = rpc.userService.forgot_service(request_data)  # call the forgot service
        response = json.dumps(response)
    return Response(response=response, content_type='application/json', status=200)


@app.route('/reset/<string:token>', methods=['PUT'])
@swag_from('new_user_swagger.yml')
def reset(**kwargs):
    request_data = json.loads(request.get_data(as_text=True))
    request_data['token'] = kwargs.get('token')
    with ClusterRpcProxy(CONFIG) as rpc:  # using cluster rpc
        response = rpc.userService.reset_password_service(request_data)  # call the reset service
        response = json.dumps(response)
    return Response(response=response, content_type='application/json', status=200)


if __name__ == "__main__":
    app.run(debug=True)
