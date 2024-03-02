from datetime import datetime
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from core import models


def create_user(email='user@example.com', password='test123123123', nickname='test'):
    # Create & Return a user
    return get_user_model().objects.create_user(
        email=email,
        password=password,
        nickname=nickname
    )


class PublicReviewAPITest(APITestCase):
    '''Test unauthenticated API requests'''

    def test_auth_required(self):
        '''Test auth required for post'''
        res = self.client.post(reverse('review:review-list'))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateReviewAPITest(APITestCase):
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
            time=time_obj,
            status='complete'
        )

        self.review = models.Review.objects.create(
            transaction=self.transaction,
            reviewer=self.buyer,
            receiver=self.seller,
            review="test review",
            rating="5"
        )

    def test_list_review(self):
        '''Test user retrieving a list of reviews'''

        res = self.client.get(reverse('review:review-list'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 1)

    def test_create_review(self):
        '''Test user creating a review'''
        self.client.force_authenticate(self.seller)
        payload = {
            'review': 'it was a good selling experience.',
            'rating': '5'
        }

        url = reverse('transaction:review-create', args=[self.transaction.id])
        res = self.client.post(url, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        review = models.Review.objects.get(review=payload['review'])
        self.assertEqual(review.reviewer, self.seller)

    def test_error_create_a_duplicate_review(self):
        '''Test error on user creating a duplicate review'''
        payload = {
            'review': 'it was a good buying experience.',
            'rating': '5'
        }

        url = reverse('transaction:review-create', args=[self.transaction.id])
        res = self.client.post(url, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data["message"], "Review already exists.")

    def test_error_incomplete_transaction_user_create_a_review(self):
        '''Test error user trying to create a review on incomplete transaction'''
        self.transaction.status = 'reserved'
        self.transaction.save()

        self.client.force_authenticate(self.seller)

        payload = {
            'review': 'it was a good buying experience.',
            'rating': '5'
        }

        url = reverse('transaction:review-create', args=[self.transaction.id])
        res = self.client.post(url, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_a_review(self):
        '''Test user retrieving a review'''
        url = reverse("review:review-detail", args=[self.review.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['review'], "test review")
