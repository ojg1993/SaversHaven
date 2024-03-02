from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.models import Category
from product.serializers import CategorySerializer

CATEGORY_URL = reverse('product:category-list')


def detail_url(category_id):
    # Create and return a category detail URL
    return reverse("product:category-detail", args=[category_id])


def create_user(email='user@example.com', password='test123123123'):
    # Create & Return a user
    return get_user_model().objects.create_user(email=email, password=password)


def create_superuser(email='admin@example.com', password='test123123123'):
    # Create & Return a user
    return get_user_model().objects.create_superuser(email=email, password=password)


class PublicCategoryAPITest(APITestCase):
    '''Test unauthenticated API requests'''

    def test_auth_required(self):
        '''Test auth required'''
        res = self.client.post(CATEGORY_URL)
        self.client.get(CATEGORY_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateCategoryAPITest(APITestCase):
    '''Test authenticated API requests'''

    def setUp(self):
        self.user = create_superuser()
        self.client.force_authenticate(self.user)

    def test_admin_user_city_list(self):
        '''Test admin user retrieving the category list'''
        category = Category.objects.create(name='Test Category')

        res = self.client.get(CATEGORY_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 1)
        self.assertEqual(res.data['results'][0]['id'], category.id)

    def test_admin_user_category_create(self):
        '''Test admin user creating a category'''
        payload = {'name': 'Test category'}
        res = self.client.post(CATEGORY_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['name'], payload['name'])

    def test_error_normal_user_create_category(self):
        '''Test returning error when a normal user try to create a category'''
        user = create_user()
        self.client.force_authenticate(user)

        payload = {'name': 'Test category'}
        res = self.client.post(CATEGORY_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_category_detail(self):
        '''Test retrieving a category'''
        category = Category.objects.create(name='Test Category')
        serializer = CategorySerializer(category)

        res = self.client.get(detail_url(category.id))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_update_city_detail(self):
        '''Test updating category detail'''
        category = Category.objects.create(name='Test Category')
        payload = {'name': 'Update category'}

        res = self.client.patch(detail_url(category.id), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        category.refresh_from_db()
        self.assertEqual(category.name, payload['name'])

    def test_delete_city_detail(self):
        '''Test deleting a category'''
        category = Category.objects.create(name='Test Category')
        res = self.client.delete(detail_url(category.id))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Category.objects.filter(id=category.id).exists())
