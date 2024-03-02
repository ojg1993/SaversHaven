from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from address.serializers import CountySerializer
from core.models import Country, County

COUNTY_URL = reverse('address:county-list')


def detail_url(county_id):
    # Create and return a county detail URL
    return reverse("address:county-detail", args=[county_id])


def create_user(email='user@example.com', password='test123123123'):
    # Create & Return a user
    return get_user_model().objects.create_user(email=email, password=password)


def create_superuser(email='admin@example.com', password='test123123123'):
    # Create & Return a user
    return get_user_model().objects.create_superuser(email=email, password=password)


class PublicCountyAPITest(APITestCase):
    '''Test unauthenticated API requests'''

    def test_auth_required(self):
        '''Test auth required'''
        res = self.client.post(COUNTY_URL)
        self.client.get(COUNTY_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateCountyAPITest(APITestCase):
    '''Test authenticated API requests'''

    def setUp(self):
        self.user = create_superuser()
        self.client.force_authenticate(self.user)

    def test_admin_user_county_list(self):
        '''Test admin user retrieving the county list'''
        c = Country.objects.create(name='Test')
        c1 = County.objects.create(name='Test County', country=c)
        c2 = County.objects.create(name='Test County2', country=c)

        res = self.client.get(COUNTY_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 2)
        self.assertEqual(res.data['results'][1]['name'], c1.name)
        self.assertEqual(res.data['results'][0]['name'], c2.name)
        self.assertEqual(res.data['results'][0]['id'], c2.id)

    def test_admin_user_county_create(self):
        '''Test admin user retrieving the county list'''
        c = Country.objects.create(name='Test')
        payload = {'name': 'Test County', 'country': c.id}
        res = self.client.post(COUNTY_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['name'], payload['name'])

    def test_normal_user_county_create_returning_error(self):
        '''Test normal user trying to create a county'''
        user = create_user()
        self.client.force_authenticate(user)

        c = Country.objects.create(name='Test')
        payload = {'name': 'Test County', 'country': c}
        res = self.client.post(COUNTY_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_county_detail(self):
        '''Test retrieving county detail'''
        c = Country.objects.create(name='Test')
        county = County.objects.create(name='Test county', country=c)
        serializer = CountySerializer(county)

        res = self.client.get(detail_url(county.id))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_update_county_detail(self):
        '''Test updating county detail'''
        c = Country.objects.create(name='Test')
        county = County.objects.create(name='Test county', country=c)
        payload = {'name': 'Update county'}

        res = self.client.patch(detail_url(county.id), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        county.refresh_from_db()
        self.assertEqual(county.name, payload['name'])

    def test_delete_county_detail(self):
        '''Test delete a county'''
        c = Country.objects.create(name='Test')
        county = County.objects.create(name='Test county', country=c)
        res = self.client.delete(detail_url(county.id))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(County.objects.filter(id=county.id).exists())
