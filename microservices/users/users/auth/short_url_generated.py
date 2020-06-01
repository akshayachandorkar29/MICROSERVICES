"""
This file contain business logic for generating random string of length 10 combining abcd....., ABCD........ and 123...
Author: Akshaya Revaskar
Date: 28/04/2020
"""
import random
import string


class ShortUrlGenerator:
    """
    This is the class for generating random string which is combination of letters and digits
    """

    def short_url(self, string_length):
        """
        Generate a random string of letters and digits
        :param string_length: length of the string required
        :return: a string
        """
        letters_and_digits = string.ascii_letters + string.digits
        return ''.join(random.choice(letters_and_digits) for i in range(string_length))
