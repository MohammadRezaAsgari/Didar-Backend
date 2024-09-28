from django.urls import resolve, reverse
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from users.api.v1.views import (
    LoginPasswordAPIView,
    LogOutAPIView,
    UserProfileAPIView,
)
from users.models import User
from users.factories import UserFactory
from utils.api.error_objects import ErrorObject


class TestLoginPasswordAPIView(APITestCase):
    def setUp(self):
        self.url = reverse('users:v1:login_password')
        self.email = 'roham@didar.com'
        self.password = 'roham@pass2022'
        self.user_obj = UserFactory(email=self.email, password=self.password)

    def test_login_bad_request(self):
        invalid_data = {'password': self.password}
        response = self.client.post(self.url, invalid_data)
        json_response = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json_response.get('success'), False)
        self.assertEqual(json_response.get('error').get(
            'code'), ErrorObject.BAD_REQUEST['code'])
        self.assertEqual(json_response.get('error').get(
            'msg'), ErrorObject.BAD_REQUEST['msg'])

    def test_login_not_found(self):
        data = {
            'username': 'wrong_username',
            'password': self.password,
        }
        response = self.client.post(self.url, data)
        json_response = response.json()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json_response.get('success'), False)
        self.assertEqual(
            json_response.get('error').get(
                'code'), ErrorObject.USER_NOT_FOUND['code']
        )
        self.assertEqual(json_response.get('error').get(
            'msg'), ErrorObject.USER_NOT_FOUND['msg'])

    def test_login_not_activated(self):
        self.user_obj.is_active = False
        self.user_obj.save()
        data = {
            'username': self.user_obj.username,
            'password': self.password,
        }
        response = self.client.post(self.url, data)
        json_response = response.json()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json_response.get('success'), False)
        self.assertEqual(
            json_response.get('error').get(
                'code'), ErrorObject.USER_NOT_FOUND['code']
        )
        self.assertEqual(json_response.get('error').get(
            'msg'), ErrorObject.USER_NOT_FOUND['msg'])

    def test_login_successful(self):
        data = {
            'username': self.user_obj.username,
            'password': self.password,
        }
        response = self.client.post(self.url, data)
        json_response = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response.get('success'), True)
        self.assertIn('access', json_response.get('data'))
        self.assertIn('refresh', json_response.get('data'))
        self.assertIn('gender', json_response.get('data'))
        self.assertIn('access_token_expires_at', json_response.get('data'))

    def test_resolve_url(self):
        resolver = resolve('/api/v1/auth/login-password/')
        self.assertEqual(resolver.view_name, 'users:v1:login_password')
        self.assertEqual(resolver.func.view_class, LoginPasswordAPIView)
        self.assertEqual(resolver.namespace, 'users:v1')
        self.assertEqual(resolver.url_name, 'login_password')


class TestUserProfileAPIView(APITestCase):
    def setUp(self):
        self.url = reverse('users:v1:user_profile')
        self.email = 'roham@didar.com'
        self.password = 'roham@pass2022'
        self.phone = '989181111222'
        self.user_obj = UserFactory(
            email=self.email, password=self.password, phone=self.phone)

    def test_user_get_profile_success(self):
        self.client.force_authenticate(user=self.user_obj)
        response = self.client.get(self.url)
        response_json = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('success'), True)
        self.assertEqual(response_json.get('data')[
                         'first_name'], self.user_obj.first_name)
        self.assertEqual(response_json.get('data')[
                         'last_name'], self.user_obj.last_name)
        self.assertEqual(response_json.get('data')['phone'], '989181***222')
        self.assertEqual(response_json.get('data')[
                         'gender'], self.user_obj.gender)

    def test_user_update_profile_success(self):
        self.client.force_authenticate(user=self.user_obj)
        data = {
            'first_name': "updated first name",
            'last_name': "updated last name",
            'phone': "+989182221111",
        }
        response = self.client.patch(self.url, data)
        self.assertEqual(response.status_code, 204)

    def test_resolve_url(self):
        resolver = resolve(f'/api/v1/auth/me/')
        self.assertEqual(resolver.view_name, 'users:v1:user_profile')
        self.assertEqual(resolver.func.view_class, UserProfileAPIView)
        self.assertEqual(resolver.namespace, 'users:v1')
        self.assertEqual(resolver.url_name, 'user_profile')


class TestLogOutAPIView(APITestCase):
    def setUp(self):
        self.url = reverse("user:v1:logout")
        self.phone = "+989123456789"
        self.email = "roham.1234@yahoo.com"
        self.password = 'roham@pass2022'
        self.user_obj = UserFactory(
            email=self.email, password=self.password, phone=self.phone)
        self.refresh = RefreshToken.for_user(self.user_obj)

    def test_logout_bad_request(self):
        invalid_data = {
            "x": "xx",
        }
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.refresh.access_token}")
        response = self.client.post(self.url, invalid_data)
        json_response = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json_response.get("success"), False)
        self.assertEqual(json_response.get("error").get(
            "code"), ErrorObject.BAD_REQUEST["code"])
        self.assertEqual(json_response.get("error").get(
            "msg"), ErrorObject.BAD_REQUEST["msg"])

    def test_logout_successful(self):
        data = {
            "refresh": str(self.refresh),
        }
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.refresh.access_token}")
        response = self.client.post(self.url, data)
        json_response = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response.get("success"), True)
        self.assertEqual(json_response.get("data"), {})

    def test_view_url_location(self):
        resolver = resolve('/api/v1/auth/logout/')
        self.assertEqual(resolver.view_name, 'users:v1:logout')
        self.assertEqual(resolver.func.cls, LogOutAPIView)
        self.assertEqual(resolver.namespace, 'users:v1')
        self.assertEqual(resolver.url_name, 'logout')
