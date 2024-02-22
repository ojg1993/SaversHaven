from datetime import datetime
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from core import models

TRANSACTION_URL = reverse('transaction:direct-transaction-list')


def detail_url(transaction_id):
    # Create and return a direct transaction detail URL
    return reverse("transaction:direct-transaction-detail", args=[transaction_id])


def create_user(email='user@example.com', password='test123123123', nickname='test'):
    # Create & Return a user
    return get_user_model().objects.create_user(
        email=email,
        password=password,
        nickname=nickname
    )


class PublicDirectTransactionAPITest(APITestCase):
    '''Test unauthenticated API requests'''

    def test_auth_required(self):
        '''Test auth required for post'''
        res = self.client.post(TRANSACTION_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateDirectTransactionAPITest(APITestCase):
    '''Test authenticated API requests'''
    def setUp(self):

        country = models.Country.objects.create(name='test country')
        county = models.County.objects.create(country=country, name='test country')
        self.city = models.City.objects.create(county=county, name='test country')
        self.user = create_user()
        self.seller = create_user(
            email='user2@example.com',
            password='test123!@#!@#',
            nickname='testSeller'
        )
        self.buyer = create_user(
            email='user3@example.com',
            password='test123!@#!@#',
            nickname='testBuyer'
        )
        self.client.force_authenticate(self.buyer)
        category = models.Category.objects.create(name='test category')
        product = models.Product.objects.create(
            seller=self.seller,
            category=category,
            title='test title',
            price=Decimal('1.00'),
            description='test description',
        )
        self.chatroom = models.ChatRoom.objects.create(
            product=product,
            seller=self.seller,
            buyer=self.buyer
        )

        self.json_time = "2024-02-20-18:00"
        time_obj = datetime.strptime(self.json_time, '%Y-%m-%d-%H:%M')
        time_obj = time_obj.replace(tzinfo=timezone.utc)
        self.transaction = models.DirectTransaction.objects.create(
            chatroom=self.chatroom,
            location=self.city,
            location_detail="at Starbucks",
            time=time_obj
        )

    def test_list_direct_transaction(self):
        '''Test user retrieving a list of direct transactions'''

        res = self.client.get(TRANSACTION_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)

    def test_create_direct_transaction(self):
        '''Test user creating a transaction'''

        payload = {
            'chatroom': self.chatroom.id,
            'time': '2024-02-22-13:30',
            'location': self.city.id,
            'location_detail': 'test',
            'status': 'reserved'
        }

        res = self.client.post(TRANSACTION_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['location_detail'], payload['location_detail'])

    def test_retrieve_a_direct_transaction(self):
        '''Test user retrieving a direct transaction'''
        res = self.client.get(detail_url(self.transaction.id))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['chatroom'], self.chatroom.id)

    def test_error_user_trying_to_retrieve_other_user_direct_transaction(self):
        '''Test error on a user trying to retrieve other user's transaction'''
        self.client.force_authenticate(self.user)
        res = self.client.get(detail_url(self.transaction.id))
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_direct_transaction(self):
        '''Test user update a transaction'''

        payload = {
            'chatroom': self.chatroom.id,
            'time': '2024-02-22-13:30',
            'location': self.city.id,
            'location_detail': 'test',
            'status': 'complete'
        }

        res = self.client.put(detail_url(1), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['status'], payload['status'])
        self.assertNotEqual(res.data['time'], self.json_time)

    def test_partial_update_direct_transaction(self):
        '''Test user partial update a transaction'''

        payload = {
            'status': 'complete'
        }

        self.assertNotEqual(self.transaction.status, payload['status'])
        res = self.client.patch(detail_url(1), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['status'], payload['status'])

    def test_delete_direct_transaction(self):
        '''Test user delete a transaction'''

        res = self.client.delete(detail_url(1))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(models.DirectTransaction.objects.exists())
