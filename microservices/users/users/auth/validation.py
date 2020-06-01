"""
This is the file for validating user's credentials
Author: Akshaya Revaskar
Date: 28/04/2020
"""
import re


class Validation:
    """
    This is the class having methods to validate user credentials with regex
    """
    def username_validate(self, username):
        """
        this is the method to validate username
        :param username: username of user
        :return: Boolean value
        """
        # This function is used to check username is in valid format or not and return true or false value
        if re.match(r"(^[a-zA-Z][a-zA-Z0-9_-]{3,16}$)", username):
            return True
        return False

    def email_validate(self, email):
        """
        this is the method to validate email
        :param email: email of user
        :return: Boolean value
        """
        # This function is used to check email is in valid format or not and return true or false value
        if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
            return True
        return False

    def password_validate(self, password):
        """
        this is the method to validate password
        :param password: password given by user
        :return: Boolean value
        """
        # This function is used to check psw is in valid format or not and return true and false value
        if re.match(r"([A-Za-z0-9@#$%^&+=]{8,})", password):
            return True
        return False