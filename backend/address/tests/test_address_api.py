from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from address.serializers import AddressSerializer
from core.models import Address, City, Country, County

ADDRESS_URL = reverse('address:address-list')


def detail_url(address_id):
    # Create and return an address detail URL
    return reverse("address:address-detail", args=[address_id])


def create_user(email='user@example.com', password='test123123123'):
    # Create & Return a user
    return get_user_model().objects.create_user(email=email, password=password)


def create_superuser(email='admin@example.com', password='test123123123'):
    # Create & Return a user
    return get_user_model().objects.create_superuser(email=email, password=password)


class PublicAddressAPITest(APITestCase):
    '''Test unauthenticated API requests'''

    def test_auth_required(self):
        '''Test auth required'''
        res = self.client.post(ADDRESS_URL)
        self.client.get(ADDRESS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateAddressAPITest(APITestCase):
    '''Test authenticated API requests'''

    def setUp(self):
        self.user = create_superuser()
        self.client.force_authenticate(self.user)

    def test_admin_user_address_list(self):
        '''Test admin user retrieving the city list'''
        country = Country.objects.create(name='Test country')
        county = County.objects.create(name='Test county', country=country)
        city = City.objects.create(name='Test city', county=county)
        address = Address.objects.create(user=self.user,
                                         post_code='123123',
                                         city=city,
                                         street_address1='Test street1',
                                         street_address2='Test street2',
                                         )
        address2 = Address.objects.create(user=self.user,
                                          post_code='456456',
                                          city=city,
                                          street_address1='Test street1',
                                          street_address2='Test street2',
                                          )

        res = self.client.get(ADDRESS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data[0]['id'], address.id)
        self.assertEqual(res.data[1]['post_code'], address2.post_code)

    def test_admin_user_address_create(self):
        '''Test admin user creating an address'''
        country = Country.objects.create(name='Test country')
        county = County.objects.create(name='Test county', country=country)
        city = City.objects.create(name='Test city', county=county)

        payload = {'user': self.user.id,
                   'name': 'test name',
                   'post_code': '123123',
                   'city': city.id,
                   'street_address1': 'Test street1',
                   'street_address2': 'Test street2'
                   }
        res = self.client.post(ADDRESS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['post_code'], payload['post_code'])

    def test_normal_user_city_create_returning_error(self):
        '''Test normal user trying to create a city'''
        user = create_user()
        self.client.force_authenticate(user)

        country = Country.objects.create(name='Test country')
        county = County.objects.create(name='Test county', country=country)
        city = City.objects.create(name='Test city', county=county)

        payload = {'user': self.user,
                   'post_code': '123123',
                   'city': city,
                   'street_address1': 'Test street1',
                   'street_address2': 'Test street2'
                   }

        res = self.client.post(ADDRESS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_address_detail(self):
        '''Test retrieving address detail'''
        country = Country.objects.create(name='Test country')
        county = County.objects.create(name='Test county', country=country)
        city = City.objects.create(name='Test city', county=county)
        address = Address.objects.create(user=self.user,
                                         post_code='123123',
                                         city=city,
                                         street_address1='Test street1',
                                         street_address2='Test street2',
                                         )
        serializer = AddressSerializer(address)

        res = self.client.get(detail_url(address.id))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_update_address_detail(self):
        '''Test updating address detail'''
        country = Country.objects.create(name='Test country')
        county = County.objects.create(name='Test county', country=country)
        city = City.objects.create(name='Test city', county=county)
        address = Address.objects.create(user=self.user,
                                         post_code='123123',
                                         city=city,
                                         street_address1='Test street1',
                                         street_address2='Test street2',
                                         )
        payload = {'post_code': 'updated'}

        res = self.client.patch(detail_url(address.id), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        city.refresh_from_db()
        self.assertEqual(res.data['post_code'], payload['post_code'])

    def test_delete_address_detail(self):
        '''Test delete an address'''
        country = Country.objects.create(name='Test country')
        county = County.objects.create(name='Test county', country=country)
        city = City.objects.create(name='Test city', county=county)
        address = Address.objects.create(user=self.user,
                                         post_code='123123',
                                         city=city,
                                         street_address1='Test street1',
                                         street_address2='Test street2',
                                         )

        res = self.client.delete(detail_url(address.id))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Address.objects.filter(id=address.id).exists())
