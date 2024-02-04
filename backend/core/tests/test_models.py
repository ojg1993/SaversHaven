from django.contrib.auth import get_user_model
from django.test import TestCase

from core import models


def create_user(email='user@example.com', password='test123'):
    '''Create and return a test user'''
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    def test_register_user_with_email_successful(self):
        '''Test creating a new user with an email'''

        user = create_user()
        self.assertEqual(user.email, 'user@example.com')
        self.assertTrue(user.check_password('test123'))

    def test_new_user_email_normalised(self):
        '''Test email for a new user is normalized'''

        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com']
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email=email,
                                                        password='sample123'
                                                        )
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raising_error(self):
        '''Test creating a user without an email raises an error'''
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        '''Test creating a superuser'''
        user = get_user_model().objects.create_superuser('test@example.com', 'test123')
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_country(self):
        '''Test creating a country'''
        country = models.Country.objects.create(name='test country')
        self.assertEqual(str(country), country.name)

    def test_create_county(self):
        '''Test creating a country'''
        country = models.Country.objects.create(name='test country')
        county = models.County.objects.create(country=country, name='test country')
        self.assertEqual(str(county), county.name)

    def test_create_city(self):
        '''Test creating a city'''
        country = models.Country.objects.create(name='test country')
        county = models.County.objects.create(country=country, name='test country')
        city = models.City.objects.create(county=county, name='test country')
        self.assertEqual(str(city), city.name)

    def test_create_address(self):
        '''Test creating address'''
        user = create_user()
        country = models.Country.objects.create(name='test country')
        county = models.County.objects.create(country=country, name='test country')
        city = models.City.objects.create(county=county, name='test country')
        address = models.Address.objects.create(
            user=user,
            post_code='12345',
            city=city,
            street_address1='test street1',
            street_address2='test street2'
        )
        self.assertEqual(str(address), f'{user.nickname} - {address.name}')

    def test_get_address_full_name(self):
        '''Test retrieving a full address'''
        user = create_user()
        country = models.Country.objects.create(name='test country')
        county = models.County.objects.create(country=country, name='test county')
        city = models.City.objects.create(county=county, name='test country')
        address = models.Address.objects.create(
            user=user,
            post_code='12345',
            city=city,
            street_address1='test street1',
            street_address2='test street2'
        )
        self.assertEqual(address.get_full_address(),
                         (country.name,
                          address.post_code,
                          county.name,
                          city.name,
                          address.street_address1,
                          address.street_address2)
                         )
