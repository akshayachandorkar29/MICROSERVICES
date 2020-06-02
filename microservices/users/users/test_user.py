import json
import requests
from .common.utils import *
baseurl = "http://127.0.0.1:9002"


class TestRegistration:

    def test_registration_username_starting_with_letter(self):
        url = baseurl + '/register'
        data = {'username': '3425sunita', 'password': 'sunita@29', 'email': 'mudaliarsunita29@gmail.com'}
        headers = {'content_type': "application/json"}
        res = requests.post(url=url, data=json.dumps(data), headers=headers)
        print(res.text)
        assert res.status_code == 200

    def test_registration_username_is_number(self):
        url = baseurl + '/register'
        data = {'username': '342545', 'password': 'sunita@29', 'email': 'mudaliarsunita29@gmail.com'}
        headers = {'content_type': "application/json"}
        res = requests.post(url=url, data=json.dumps(data), headers=headers)
        print(res.text)
        assert res.status_code == 200

    def test_registration_username_is_less_than_4(self):
        url = baseurl + '/register'
        data = {'username': 'sun', 'password': 'sunita@29', 'email': 'mudaliarsunita29@gmail.com'}
        headers = {'content_type': "application/json"}
        res = requests.post(url=url, data=json.dumps(data), headers=headers)
        print(res.text)
        assert res.status_code == 200

    def test_registration_username_is_greater_than_16(self):
        url = baseurl + '/register'
        data = {'username': 'sunitabalkrishnamudaliar', 'password': 'sunita@29', 'email': 'mudaliarsunita29@gmail.com'}
        headers = {'content_type': "application/json"}
        res = requests.post(url=url, data=json.dumps(data), headers=headers)
        print(res.text)
        assert res.status_code == 200

    def test_registration_password_is_less_than_8(self):
        url = baseurl + '/register'
        data = {'username': 'sunita', 'password': 'sunita', 'email': 'mudaliarsunita29@gmail.com'}
        headers = {'content_type': "application/json"}
        res = requests.post(url=url, data=json.dumps(data), headers=headers)
        print(res.text)
        assert res.status_code == 200

    def test_registration_email_missing_at_the_rate(self):
        url = baseurl + '/register'
        data = {'username': 'sunita', 'password': 'sunita@29', 'email': 'mudaliarsunita29gmail.com'}
        headers = {'content_type': "application/json"}
        res = requests.post(url=url, data=json.dumps(data), headers=headers)
        print(res.text)
        assert res.status_code == 200

    def test_registration_email_missing_dot(self):
        url = baseurl + '/register'
        data = {'username': 'sunita', 'password': 'sunita@29', 'email': 'mudaliarsunita29@gmailcom'}
        headers = {'content_type': "application/json"}
        res = requests.post(url=url, data=json.dumps(data), headers=headers)
        print(res.text)
        assert res.status_code == 200