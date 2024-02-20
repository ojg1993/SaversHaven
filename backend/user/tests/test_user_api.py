from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

REGISTER_URL = reverse('user:register')
TOKEN_LOGIN_URL = reverse('user:login')


def create_user(**parmas):
    return get_user_model().objects.create_user(**parmas)


class PublicUserApiTest(APITestCase):
    '''Test the public features of the Account API'''
    def setUp(self):
        self.test_user = create_user(email='login@test.com', password='test123123123')

    def test_register_successful(self):
        '''Test creating a new user'''
        payload = {
            'email': 'test@test.com',
            'password': 'test123123123',
            'nickname': 'test',
            'first_name': 'test',
            'last_name': 'test',
            'phone_number': '123123123',
        }

        res = self.client.post(REGISTER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_register_error_existing_email(self):
        '''Test returning an error if email is already taken'''
        payload = {
            'email': 'test@test.com',
            'password': 'test123',
            'nickname': 'test',
            'first_name': 'test',
            'last_name': 'test',
            'phone_number': '123123123',
        }

        create_user(**payload)

        res = self.client.post(REGISTER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_error_password_shorter_than_10(self):
        '''Test returning an error if password is too short'''
        payload = {
            'email': 'test@test.com',
            'password': '12',
            'nickname': 'test',
            'first_name': 'test',
            'last_name': 'test',
            'phone_number': '123123123',
        }

        res = self.client.post(REGISTER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = (get_user_model()
                       .objects.filter(email=payload['email'])
                       .exists())
        self.assertFalse(user_exists)

    def test_token_login_successful(self):
        '''Test login successful'''
        payload = {
            'email': 'login@test.com',
            'password': 'test123123123'
        }
        res = self.client.post(TOKEN_LOGIN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_token_login_error_invalid_password(self):
        '''Test login error with invalid password'''
        payload = {
            'email': 'login@test.com',
            'password': '123123'
        }
        res = self.client.post(TOKEN_LOGIN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_token_login_error_blank_password(self):
        '''Test login error with a blank password'''
        payload = {
            'email': 'login@test.com',
            'password': '',
        }
        res = self.client.post(TOKEN_LOGIN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)
