"""
This is the service file which has all the business logic of user service
Author: Akshaya Revaskar
Date: 29-04-2020
"""

# importing necessary modules and packages
from nameko.rpc import rpc
from .common.db_operations import *
from .models import Users, Short
from .config.redis_connection import RedisConnection
from .auth.short_url_generated import ShortUrlGenerator
from .vendor.send_mail import SendMail
from .auth.validation import Validation
from ..users_env import Configuration
import jwt

configuration = Configuration()
short_object = ShortUrlGenerator()
redis_obj = RedisConnection()
mail_obj = SendMail()
valid = Validation()


class UserService(object):
    name = 'userService'

    # service for registering users
    @rpc
    def registration_service(self, request_data):
        """
        this is the method for registering user
        :param request_data: json data coming from user
        :return: response dictionary with message, data and success flag
        """

        response = {
            "success": False,
            "message": "something went wrong!",
            "data": []
        }

        try:
            # unpacking data from request object
            username = request_data.get('username')
            password = request_data.get('password')
            email = request_data.get('email')

            # validating username
            if not valid.username_validate(username):
                response["message"] = "Length of Username should be greater than 3 and less than 16 " \
                                      "and it can not be a number"
                raise ValueError

            # validating email
            if not valid.email_validate(email):
                response["message"] = "Not a valid email id"
                raise ValueError

            # validating password
            if not valid.password_validate(password):
                response["message"] = "Length of password must be 8 or more!!!"
                raise ValueError

            record = filter_by_email(table=Users, email=email)
            if not record:
                user_data = Users(username=username,
                                  password=password,
                                  email=email)

                # saving user object in the database
                save(user_data)

                # retrieving record of the current user to get id
                db_record = filter_by_email(table=Users, email=email)
                if db_record:
                    user_id = db_record.id

                    # generating jwt token with user id
                    token = jwt.encode({'id': user_id}, configuration.JWT_SECRET_KEY, algorithm='HS256').decode(
                        'utf-8')

                    # generating short url
                    short = short_object.short_url(10)

                    short_data = Short(token=token,
                                       short=short)
                    # saving short object into database
                    save(short_data)

                    host = configuration.MICRO_HOST
                    port = configuration.MICRO_PORT
                    html_file_name = 'users/users/activate.html'

                    # sending mail using token, email id and link
                    mail_obj.send_mail(email, username, host, port, short, html_file_name)

                    response["success"] = True
                    response["message"] = "User Registered successfully!"

            else:
                response["message"] = "User Already Exist"

        # catching exceptions
        except ValueError:
            response = response

        except Exception:
            response = response

        return response

    # service for activating registered user
    @rpc
    def activate_registration_service(self, request_data):
        """
        this is the method for activating user by updating active flag
        :param request_data: json data coming from user
        :return: response dictionary with message, data and success flag
        """

        response = {
            "success": False,
            "message": "something went wrong!",
            "data": []
        }
        try:

            # getting data from the link
            short_token = request_data.get('token')
            short_token = short_token.split("=")
            short_token = short_token[1]
            if short_token is not None:  # if the short url is not empty,

                # getting respective token from given short url
                result = filter_by_short(Short, short_token)
                if result:
                    token = result.token

                    # decoding token
                    payload = jwt.decode(token, configuration.JWT_SECRET_KEY, algorithms=['HS256'])
                    user_id = payload.get('id')

                    # activating user
                    result = update_active(table=Users, id=user_id)
                    if result:
                        response["success"] = True
                        response["message"] = "Your account is activated Successfully!"
                    else:
                        response["message"] = "user does not exist"

        except Exception:
            response = response

        return response

    # user login service
    @rpc
    def login_service(self, request_data):
        """
        this is the method for logging user in
        :param request_data:
        :return: response dictionary with message, data and success flag
        """
        response = {
            "success": False,
            "message": "Unable to login",
            "data": []
        }
        try:
            # getting data from request object
            email = request_data.get('email')
            password = request_data.get('password')

            db_record = filter_by_email(table=Users, email=email)
            if db_record:
                user_id = db_record.id
                if db_record.password == password and db_record.active == 1:

                    # generating token using JWT module
                    token = jwt.encode({'id': user_id}, configuration.JWT_SECRET_KEY, algorithm='HS256').decode('utf-8')

                    # setting data into redis cache
                    redis_obj.set(user_id, token)

                    response["success"] = True
                    response["message"] = "Successfully logged in!"
                    response["data"] = [{"token": token}]

        except Exception:
            response = response

        return response

    # service for forget password
    @rpc
    def forgot_service(self, request):
        """
        this is the method for allowing user to tell that they forgot the password
        :param request: json data coming from user
        :return: response dictionary with message, data and success flag
        """
        response = {
            "success": False,
            "message": "Something went wrong",
            "data": []
        }
        try:

            username = request.get('username')
            email = request.get('email')

            result = filter_by_email(table=Users, email=email)
            if result:
                user_id = result.id

                # generating token with JWT module
                token = jwt.encode({'id': user_id}, configuration.JWT_SECRET_KEY, algorithm='HS256').decode('utf-8')

                # generating short url
                short = short_object.short_url(10)

                short_data = Short(token=token,
                                   short=short)
                # saving short object into database
                save(short_data)

                host = configuration.MICRO_HOST
                port = configuration.MICRO_PORT
                html_file_name = 'users/users/forgot.html'

                # sending mail using token, email id and link
                mail_obj.send_mail(email, username, host, port, short, html_file_name)

                response["success"] = True
                response["message"] = "Mail sent successfully!"

            else:
                response["message"] = "User Not found"

        except Exception:
            response = response

        return response

    # service for resetting password in case of forget
    @rpc
    def reset_password_service(self, request):
        """
        this is the method for resetting password
        :param request: json data coming from user
        :return: response dictionary with message, data and success flag
        """
        response = {
            "success": False,
            "message": "Something went wrong!",
            "data": []
        }
        try:

            # getting data from request object
            email = request.get('email')
            old_password = request.get('old_password')
            new_password = request.get('new_password')

            short_token = request.get('token')
            short_token = short_token.split("=")
            short_token = short_token[1]

            if short_token is not None:
                result = filter_by_short(Short, short_token)
                if result:
                    token = result.token

                    # decoding token
                    payload = jwt.decode(token, 'secret', algorithms=['HS256'])
                    user_id = payload.get('id')

                    # updating new password in the database
                    update_result = update_password(table=Users, id=user_id, new_password=new_password)

                    if update_result:
                        response["message"] = "Password reset Successfully!!!"
                        response["success"] = True

                else:
                    response["message"] = "Token not found!!!"

        except Exception:
            response = response

        return response
