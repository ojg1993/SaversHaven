from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from django.test import override_settings


REGISTER_URL = 'http://localhost:8000/api/auth/registration/'
LOGIN_URL = 'http://localhost:8000/api/auth/login/'


def create_user(**parmas):
    return get_user_model().objects.create_user(**parmas)

@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class PublicUserApiTest(APITestCase):
    '''Test the public features of the Account API'''

    def setUp(self):
        self.test_user = create_user(email='login@test.com', password='test123123123')
    def test_register_successful(self):
        '''Test creating a new user'''
        payload = {
            'email': 'ojgpo@naver.com',
            'password1': 'test123123123',
            'password2': 'test123123123',
            'nickname': 'test',
            'first_name': 'test',
            'last_name': 'test',
            'phone_number': '123123123',
        }

        res = self.client.post(REGISTER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['detail'], "Verification e-mail sent.")

        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password1']))

    def test_register_error_existing_email(self):
        '''Test returning an error if email is already taken'''
        payload = {
            'email': 'test@test.com',
            'password1': 'test123123123',
            'password2': 'test123123123',
            'nickname': 'test',
            'first_name': 'test',
            'last_name': 'test',
            'phone_number': '123123123',
        }

        create_user(**payload)

        res = self.client.post(REGISTER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['email'][0], 'A user is already registered with this e-mail address.')

    def test_register_error_password_shorter_than_10(self):
        '''Test returning an error if password is too short'''
        payload = {
            'email': 'test@test.com',
            'password1': '12',
            'password2': '12',
            'nickname': 'test',
            'first_name': 'test',
            'last_name': 'test',
            'phone_number': '123123123',
        }

        res = self.client.post(REGISTER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('This password is too short.', res.data['password1'][0])
        user_exists = (get_user_model()
                       .objects.filter(email=payload['email'])
                       .exists())
        self.assertFalse(user_exists)

    def test_login_successful(self):
        '''Test login successful'''
        payload = {
            'email': 'login@test.com',
            'password': 'test123123123'
        }
        res = self.client.post(LOGIN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['non_field_errors'][0], "E-mail is not verified.")

    def test_login_error_invalid_password(self):
        '''Test login error with invalid password'''
        payload = {
            'email': 'login@test.com',
            'password': '123123'
        }
        res = self.client.post(LOGIN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['non_field_errors'][0],
                         "Unable to log in with provided credentials.")

    def test_login_error_blank_password(self):
        '''Test login error with a blank password'''
        payload = {
            'email': 'login@test.com',
            'password': '',
        }
        res = self.client.post(LOGIN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['password'][0],
                         "This field may not be blank.")
