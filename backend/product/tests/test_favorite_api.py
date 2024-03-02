from decimal import Decimal

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.models import Category, Favorite, Product


def favorite_url(product_id):
    # Create and return a favorite URL
    return reverse("product:favorite", args=[product_id])


def create_user(email='user@example.com', password='test123123123'):
    # Create & Return a user
    return get_user_model().objects.create_user(email=email, password=password)


class PublicFavoriteAPITest(APITestCase):
    '''Test unauthenticated API requests'''

    def test_auth_required(self):
        '''Test auth required for favorite'''
        self.user = create_user()
        self.client.force_authenticate(self.user)
        category = Category.objects.create(name='Test Category')
        product = Product.objects.create(
            seller=self.user,
            category=category,
            title='test_product',
            price=Decimal('10.00'),
            description='test description'
        )
        self.client.force_authenticate(None)
        res = self.client.post(favorite_url(product.id))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateFavoriteAPITest(APITestCase):
    '''Test authenticated API requests'''

    def setUp(self):
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_favorite_create(self):
        category = Category.objects.create(name='Test Category')
        product = Product.objects.create(
            seller=self.user,
            category=category,
            title='test_product',
            price=Decimal('10.00'),
            description='test description'
        )

        res = self.client.post(favorite_url(product.id))
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        favorite = Favorite.objects.first()
        self.assertEqual(self.user, favorite.user)
        self.assertEqual(product, favorite.product)

    def test_favorite_delete(self):
        category = Category.objects.create(name='Test Category')
        product = Product.objects.create(
            seller=self.user,
            category=category,
            title='test_product',
            price=Decimal('10.00'),
            description='test description'
        )
        favorite = Favorite.objects.create(
            user=self.user,
            product=product
        )

        res = self.client.delete(favorite_url(product.id))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        cnt = Favorite.objects.count()
        self.assertEqual(cnt, 0)
        self.assertEqual(favorite.user, self.user)
