from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from address.serializers import CitySerializer
from core.models import City, Country, County

CITY_URL = reverse('address:city-list')


def detail_url(city_id):
    # Create and return a city detail URL
    return reverse("address:city-detail", args=[city_id])


def create_user(email='user@example.com', password='test123123123'):
    # Create & Return a user
    return get_user_model().objects.create_user(email=email, password=password)


def create_superuser(email='admin@example.com', password='test123123123'):
    # Create & Return a user
    return get_user_model().objects.create_superuser(email=email, password=password)


class PublicCityAPITest(APITestCase):
    '''Test unauthenticated API requests'''

    def test_auth_required(self):
        '''Test auth required'''
        res = self.client.post(CITY_URL)
        self.client.get(CITY_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateCityAPITest(APITestCase):
    '''Test authenticated API requests'''

    def setUp(self):
        self.user = create_superuser()
        self.client.force_authenticate(self.user)

    def test_admin_user_city_list(self):
        '''Test admin user retrieving the city list'''
        country = Country.objects.create(name='Test country')
        county = County.objects.create(name='Test county', country=country)
        city = City.objects.create(name='Test city', county=county)
        city2 = City.objects.create(name='Test city2', county=county)

        res = self.client.get(CITY_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 2)
        self.assertEqual(res.data['results'][1]['id'], city.id)
        self.assertEqual(res.data['results'][0]['name'], city2.name)

    def test_admin_user_city_create(self):
        '''Test admin user retrieving the city list'''
        country = Country.objects.create(name='Test country')
        county = County.objects.create(name='Test county', country=country)
        payload = {'name': 'Test city', 'county': county.id}
        res = self.client.post(CITY_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['name'], payload['name'])

    def test_normal_user_city_create_returning_error(self):
        '''Test normal user trying to create a city'''
        user = create_user()
        self.client.force_authenticate(user)

        country = Country.objects.create(name='Test country')
        county = County.objects.create(name='Test county', country=country)
        payload = {'name': 'Test city', 'county': county.id}
        res = self.client.post(CITY_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_city_detail(self):
        '''Test retrieving city detail'''
        country = Country.objects.create(name='Test country')
        county = County.objects.create(name='Test county', country=country)
        city = City.objects.create(name='Test city', county=county)
        serializer = CitySerializer(city)

        res = self.client.get(detail_url(city.id))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_update_city_detail(self):
        '''Test updating city detail'''
        country = Country.objects.create(name='Test country')
        county = County.objects.create(name='Test county', country=country)
        city = City.objects.create(name='Test city', county=county)
        payload = {'name': 'Update city'}

        res = self.client.patch(detail_url(city.id), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        city.refresh_from_db()
        self.assertEqual(city.name, payload['name'])

    def test_delete_city_detail(self):
        '''Test delete a city'''
        country = Country.objects.create(name='Test country')
        county = County.objects.create(name='Test county', country=country)
        city = City.objects.create(name='Test city', county=county)
        res = self.client.delete(detail_url(city.id))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(City.objects.filter(id=city.id).exists())
