from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.models import Country

COUNTRY_URL = reverse('address:country')


def create_user(email='user@example.com', password='test123123123'):
    # Create & Return a user
    return get_user_model().objects.create_user(email=email, password=password)


def create_superuser(email='admin@example.com', password='test123123123'):
    # Create & Return a user
    return get_user_model().objects.create_superuser(email=email, password=password)


class PublicCountryAPITest(APITestCase):
    '''Test unauthenticated API requests'''
    def test_auth_required(self):
        '''Test auth required'''
        res = self.client.post(COUNTRY_URL)
        self.client.get(COUNTRY_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateCountryAPITest(APITestCase):
    '''Test authenticated API requests'''
    def setUp(self):
        self.user = create_superuser()
        self.client.force_authenticate(self.user)

    def test_admin_user_country_list(self):
        '''Test admin user retrieving the country list'''
        c1 = Country.objects.create(name='Test Country')
        c2 = Country.objects.create(name='Test Country2')

        res = self.client.get(COUNTRY_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data[0]['name'], c1.name)
        self.assertEqual(res.data[1]['name'], c2.name)
        self.assertEqual(res.data[1]['id'], c2.id)

    def test_admin_user_country_create(self):
        '''Test admin user retrieving the country list'''
        payload = {'name': 'Test Country'}
        res = self.client.post(COUNTRY_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['name'], payload['name'])

    def test_normal_user_country_create_returning_error(self):
        '''Test normal user trying to create a country'''
        user = create_user()
        self.client.force_authenticate(user)
        payload = {'name': 'Test Country'}
        res = self.client.post(COUNTRY_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
