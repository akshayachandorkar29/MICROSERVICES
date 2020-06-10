"""
This is the gateway service file which has all the services related to user and note
Author: Akshaya Revaskar
Date: 29-04-2020
"""
import json
from nameko.rpc import RpcProxy
from .common.utils import *
from .auth.decorator import is_authenticated
from werkzeug.wrappers import Response
from nameko.web.handlers import http


class GatewayService:
    """
    This is the Gateway which contains two microservices: user microservice and notes microservice
    """
    name = 'gateway'
    note_rpc = RpcProxy('noteService')
    user_rpc = RpcProxy('userService')

# =============================================User Service ===========================================================

    # this is the service for registering user
    @http('POST', '/user/register')
    def registration(self, request):
        """
        This method is for user registration
        :param request: request coming from client to server
        :return: Response with response dictionary and status code
        """
        # converting request data from json to dictionary
        request_data = json.loads(request.get_data(as_text=True))
        response = self.user_rpc.registration_service(request_data)  # calling registration service
        # converting response from dictionary to json
        response = json.dumps(response)
        return Response(response=response, content_type='application/json', status=200)

    # this is the service for activating user
    @http('GET', '/user/activate/<string:token>')
    def activate_registration(self, request, **kwargs):
        """
        This method is for activating user
        :param kwargs: list of arguments with key
        :return: Response with response dictionary and status code
        """
        short_token = kwargs.get('token')
        response = self.user_rpc.activate_registration_service(short_token)  # calling activation service
        # converting response from dictionary to json
        response = json.dumps(response)
        return Response(response=response, content_type='application/json', status=200)

    # this is the service for user login
    @http('POST', '/user/login')
    def login(self, request):
        """
        This method is user login method
        :param request: request coming from client to server
        :return: Response with response dictionary and status code
        """
        # converting request data from json to dictionary
        request_data = json.loads(request.get_data(as_text=True))
        response = self.user_rpc.login_service(request_data)  # calling login service
        # converting response from dictionary to json
        response = json.dumps(response)
        return Response(response=response, content_type='application/json', status=200)

    # this is the service for allowing user to reset password in case of forgot
    @http('POST', '/user/forgot')
    def forgot(self, request):
        """
        This method gets called if user forgets the password
        :param request: request coming from client to server
        :return: Response with response dictionary and status code
        """
        # converting request data from json to dictionary
        request_data = json.loads(request.get_data(as_text=True))
        response = self.user_rpc.forgot_service(request_data)  # calling forgot service
        # converting response from dictionary to json
        response = json.dumps(response)
        return Response(response=response, content_type='application/json', status=200)

    # this is the service to reset the password
    @http('PUT', '/user/reset/<string:token>')
    @is_authenticated
    def reset_password(self, request, **kwargs):
        """
        This is the method for resetting user password
        :param request: request coming from client to server
        :param kwargs: list of arguments with keys
        :return: Response with response dictionary and status code
        """
        # converting request data from json to dictionary
        request_data = json.loads(request.get_data(as_text=True))
        request_data['token'] = kwargs.get('token')
        response = self.user_rpc.reset_password_service(request_data)  # calling reset service
        # converting response from dictionary to json
        response = json.dumps(response)
        return Response(response=response, content_type='application/json', status=200)

# ==================================================== Note Service ===================================================

    # service for creating new note
    @http('POST', '/note/create')
    @is_authenticated
    def create_note(self, request):
        """
        This is the method for creating note
        :param request: request coming from client to server
        :return: Response with response dictionary and status code
        """
        # converting request data from json to dictionary
        request_data = json.loads(request.get_data(as_text=True))
        token = request.headers['token']
        payload = decode_jwt_token(token)
        request_data['user_id'] = payload.get('id')
        response = self.note_rpc.create_note_service(request_data)  # calling create note service
        # converting response from dictionary to json
        response = json.dumps(response)
        return Response(response=response, content_type='application/json', status=200)

    # service for reading note
    @http('GET', '/note/read')
    @is_authenticated
    def read_note(self, request):
        """
        This is the method to read note
        :param request: request coming from client to server
        :param kwargs: list of arguments with keys
        :return: Response with response dictionary and status code
        """
        token = request.headers['token']
        payload = decode_jwt_token(token)
        request_data = {'user_id': payload.get('id')}
        response = self.note_rpc.read_note_service(request_data)  # calling read note service
        # converting response from dictionary to json
        response = json.dumps(response)
        return Response(response=response, content_type='application/json', status=200)

    # service for updating note
    @http('PUT', '/note/update/<string:pk>')
    @is_authenticated
    def update_note(self, request, **kwargs):
        """
        Method for updating note
        :param request: request coming from client to server
        :param kwargs: list of arguments with keys
        :return: Response with response dictionary and status code
        """
        # converting request data from json to dictionary
        request_data = json.loads(request.get_data(as_text=True))
        token = request.headers['token']
        payload = decode_jwt_token(token)
        request_data['user_id'] = payload.get('id')
        request_data['id'] = kwargs.get('pk')
        response = self.note_rpc.update_note_service(request_data)  # calling update note service
        # converting response from dictionary to json
        response = json.dumps(response)
        return Response(response=response, content_type='application/json', status=200)

    # service for pinned note
    @http('PUT', '/note/pin/<string:pk>')
    @is_authenticated
    def pin_note(self, request, **kwargs):
        """
        method for pin note
        :param request: request coming from client to server
        :param kwargs: argumet list with keys
        :return: Response with response dictionary and status code
        """
        # converting request data from json to dictionary
        request_data = json.loads(request.get_data(as_text=True))
        token = request.headers['token']
        payload = decode_jwt_token(token)
        request_data['user_id'] = payload.get('id')
        request_data['id'] = kwargs.get('pk')
        response = self.note_rpc.pin_note_service(request_data)  # calling pin note service
        # converting response from dictionary to json
        response = json.dumps(response)
        return Response(response=response, content_type='application/json', status=200)

    # service for archived note
    @http('PUT', '/note/archive/<string:pk>')
    @is_authenticated
    def archive_note(self, request, **kwargs):
        """
        method for archive note
        :param request: request coming from client to server
        :param kwargs: list of arguments with keys
        :return: Response with response dictionary nad status code
        """
        # converting request data from json to dictionary
        request_data = json.loads(request.get_data(as_text=True))
        token = request.headers['token']
        payload = decode_jwt_token(token)
        request_data['user_id'] = payload.get('id')
        request_data['id'] = kwargs.get('pk')
        response = self.note_rpc.archive_note_service(request_data)  # calling archive note service
        # converting response from dictionary to json
        response = json.dumps(response)
        return Response(response=response, content_type='application/json', status=200)

    # service for restored note
    @http('PUT', '/note/restore/<string:pk>')
    @is_authenticated
    def restore_note(self, request, **kwargs):
        """
        method for restoring note
        :param request: request coming from client to server
        :param kwargs: list of arguments with keys
        :return: Response with response dictionary and status code
        """
        # converting request data from json to dictionary
        request_data = json.loads(request.get_data(as_text=True))
        token = request.headers['token']
        payload = decode_jwt_token(token)
        request_data['user_id'] = payload.get('id')
        request_data['id'] = kwargs.get('pk')
        response = self.note_rpc.restore_note_service(request_data)  # calling restore note service
        # converting response from dictionary to json
        response = json.dumps(response)
        return Response(response=response, content_type='application/json', status=200)

    # service for deleting note
    @http('DELETE', '/note/delete/<string:pk>')
    @is_authenticated
    def delete_note(self, request, **kwargs):
        """
        method for deleting note
        :param request: request coming from client to server
        :param kwargs: list of arguments with keys
        :return: Response with response dictionary and status code
        """
        token = request.headers['token']
        payload = decode_jwt_token(token)
        request_data = dict()
        request_data['user_id'] = payload.get('id')
        request_data['id'] = kwargs.get('pk')
        response = self.note_rpc.delete_note_service(request_data)  # calling delete note service
        # converting response from dictionary to json
        response = json.dumps(response)
        return Response(response=response, content_type='application/json', status=200)

    # gateway service for listing note
    @http('GET', '/note/list')
    @is_authenticated
    def list_note(self, request):
        """
        method for listing all the notes
        :return: list of notes
        """
        request_data = json.loads(request.get_data(as_text=True))
        response = self.note_rpc.list_note_service(request_data)  # calling list note service
        # converting response from dictionary to json
        response = json.dumps(response)
        return Response(response=response, content_type='application/json', status=200)

    # service for creating label
    @http('POST', '/label/create')
    @is_authenticated
    def create_label(self, request):
        """
        method for creating label
        :param request: request coming from client to server
        :return: Response with response dictionary and status code
        """
        # converting request data from json to dictionary
        request_data = json.loads(request.get_data(as_text=True))
        token = request.headers['token']
        payload = decode_jwt_token(token)
        request_data['user_id'] = payload.get('id')
        response = self.note_rpc.create_label_service(request_data)  # calling create label service
        # converting response from dictionary to json
        response = json.dumps(response)
        return Response(response=response, content_type='application/json', status=200)

    # service for reading label
    @http('GET', '/label/read')
    @is_authenticated
    def read_label(self, request):
        """
        this is the method for reading label
        :param request: request coming from client to server
        :return: Response with response dictionary and status code
        """
        token = request.headers['token']
        payload = decode_jwt_token(token)
        request_data = {'user_id': payload.get('id')}
        response = self.note_rpc.read_label_service(request_data)  # calling read label service
        # converting response from dictionary to json
        response = json.dumps(response)
        return Response(response=response, content_type='application/json', status=200)

    # service for deleting label
    @http('DELETE', '/label/delete/<string:pk>')
    @is_authenticated
    def delete_label(self, request, **kwargs):
        """
        this is the method for deleting label
        :param request: request coming from client to server
        :param kwargs: list of arguments with keys
        :return: Response with response dictionary and status code
        """
        token = request.headers['token']
        payload = decode_jwt_token(token)
        request_data = dict()
        request_data['user_id'] = payload.get('id')
        request_data['id'] = kwargs.get('pk')
        response = self.note_rpc.delete_label_service(request_data)  # calling delete label service
        # converting response from dictionary to json
        response = json.dumps(response)
        return Response(response=response, content_type='application/json', status=200)

    # service for updating label
    @http('PUT', '/label/update/<string:pk>')
    @is_authenticated
    def update_label(self, request, **kwargs):
        """
        This method is for updating label
        :param request: with response dictionary and status code
        :param kwargs: list of arguments with keys
        :return: Response with response dictionary and status code
        """
        # converting request data from json to dictionary
        request_data = json.loads(request.get_data(as_text=True))
        token = request.headers['token']
        payload = decode_jwt_token(token)
        request_data['user_id'] = payload.get('id')
        request_data['id'] = kwargs.get('pk')
        response = self.note_rpc.update_label_service(request_data)  # calling update label service
        # converting response from dictionary to json
        response = json.dumps(response)
        return Response(response=response, content_type='application/json', status=200)