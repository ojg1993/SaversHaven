import tempfile
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.urls import reverse
from PIL import Image
from rest_framework import status
from rest_framework.test import APITestCase

from core.models import Category, Product, ProductImage
from product.serializers import ProductSerializer

PRODUCT_URL = reverse('product:product-list')


def detail_url(product_id):
    # Create and return a category detail URL
    return reverse("product:product-detail", args=[product_id])


def create_user(email='user@example.com', password='test123123123'):
    # Create & Return a user
    return get_user_model().objects.create_user(email=email, password=password)


def create_superuser(email='admin@example.com', password='test123123123'):
    # Create & Return a user
    return get_user_model().objects.create_superuser(email=email, password=password)


class PublicProductAPITest(APITestCase):
    '''Test unauthenticated API requests'''

    def test_auth_required(self):
        '''Test auth required for post'''
        res = self.client.post(PRODUCT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateProductAPITest(APITestCase):
    '''Test authenticated API requests'''

    def setUp(self):
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def tearDown(self):
        Product.objects.all().delete()

    def test_user_product_list(self):
        '''Test admin user retrieving the category list'''
        category = Category.objects.create(name='Test Category')
        product = Product.objects.create(
            seller=self.user,
            category=category,
            title='test_product',
            price=Decimal('10.00'),
            description='test description'
        )

        res = self.client.get(PRODUCT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['id'], product.id)

    def test_create_product_with_image(self):
        '''Test creating a product with an example image'''
        category = Category.objects.create(name='Test Category')

        with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
            # Create test image
            img = Image.new('RGB', (10, 10))
            # Save the test image in image_file, and convert the format to JPEG
            img.save(image_file, 'JPEG')
            # Reset the file pointer to 0 to ensure correct reading
            image_file.seek(0)

            payload = {
                'category': category.id,
                'title': 'test_product',
                'price': Decimal('10.00'),
                'description': 'test description',
                'uploaded_images': [
                    image_file
                ]
            }
            res = self.client.post(PRODUCT_URL, payload, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['title'], payload['title'])

    def test_retrieve_product_detail(self):
        '''Test retrieving a product'''
        category = Category.objects.create(name='Test Category')
        product = Product.objects.create(
            seller=self.user,
            category=category,
            title='test_product',
            price=Decimal('10.00'),
            description='test description'
        )
        serializer = ProductSerializer(product)

        res = self.client.get(detail_url(product.id))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res.data.pop('hit_cnt')  # retrieve method field
        self.assertEqual(res.data, serializer.data)

    def test_update_city_detail(self):
        '''Test updating product detail'''
        category = Category.objects.create(name='Test Category')
        product = Product.objects.create(
            seller=self.user,
            category=category,
            title='test_product',
            price=Decimal('10.00'),
            description='test description'
        )
        payload = {'title': 'update_product'}

        res = self.client.patch(detail_url(product.id), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        product.refresh_from_db()
        self.assertEqual(product.title, payload['title'])

    def test_error_other_user_update_product(self):
        '''Test returning error when other user try to update a product'''
        category = Category.objects.create(name='Test Category')
        product = Product.objects.create(
            seller=self.user,
            category=category,
            title='test_product',
            price=Decimal('10.00'),
            description='test description'
        )

        user = create_user(email='other@example.com', password='test123123123')
        self.client.force_authenticate(user)

        payload = {'title': 'forbidden attempt'}
        res = self.client.patch(detail_url(product.id), payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_product(self):
        '''Test deleting a product'''
        category = Category.objects.create(name='Test Category')
        product = Product.objects.create(
            seller=self.user,
            category=category,
            title='test_product',
            price=Decimal('10.00'),
            description='test description'
        )

        res = self.client.delete(detail_url(product.id))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(id=product.id).exists())
