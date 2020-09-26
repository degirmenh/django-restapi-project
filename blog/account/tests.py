import json

from rest_framework.test import APITestCase
from django.urls import reverse
# Create your tests here.

# register valid params
# is password invalid
# user already exist
# user already sign in

# user already sign in via token
from rest_framework_simplejwt.state import User


class UserRegistrationTestCase(APITestCase):
    url = reverse('account:register')
    url_jwt_login = reverse('token_obtain_pair')

    def test_user_registration(self):
        """ Register valid paramas """

        data = {"username": "hakantest", "email": 'degirmenhakan@gmail.com', 'password': "test8112"}

        response = self.client.post(self.url, data=data)
        self.assertEqual(201, response.status_code)

    def test_user_invalid_password(self):
        data = {"username": "hakantesxt", "email": 'degirmenhakan@gmail.com', 'password': "1"}
        response = self.client.post(self.url, data=data)
        self.assertEqual(400, response.status_code)

    def test_unique_name(self):
        self.test_user_registration()
        data = {"username": "hakantest", "email": 'degirmenhakan@gmail.com', 'password': "test8112"}
        response = self.client.post(self.url, data=data)
        self.assertEqual(400, response.status_code)

    def test_user_authenticated_registration(self):
        """ User that already sing in can not view this page """

        self.test_user_registration()
        data = {"username": "hakantest", 'password': "test8112"}
        self.client.login(username=data['username'], password=data['password'])

        response = self.client.get(self.url)
        self.assertEqual(405, response.status_code)

    def test_user_authenticated_via_token_registration(self):
        """ User that already sing in via token can not view this page """

        self.test_user_registration()
        data = {"username": "hakantest", 'password': "test8112"}
        token_resp = self.client.post(self.url_jwt_login, data)
        self.assertEqual(200, token_resp.status_code)
        print(token_resp.data)
        token = token_resp.data['access']

        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+ token)

        response = self.client.get(self.url, data)

        self.assertEqual(405, response.status_code)


class UserLogin(APITestCase):
    url_jwt_login = reverse('token_obtain_pair')

    def setUp(self):
        self.username = 'hakantest'
        self.password = 'test8112'

        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_user_token(self):
        token_resp = self.client.post(self.url_jwt_login, {'username': self.username,
                                                           'password': self.password})
        self.assertEqual(200, token_resp.status_code)

        self.assertTrue('access' in json.loads(token_resp.content))

    def test_user_invalid_data(self):
        token_resp = self.client.post(self.url_jwt_login, {'username': self.username,
                                                           'password': self.password})
        self.assertEqual(200, token_resp.status_code)

        self.assertTrue('access' in json.loads(token_resp.content))

