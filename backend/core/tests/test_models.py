from datetime import datetime
from decimal import Decimal
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from core import models


def create_user(email='user@example.com', password='test123'):
    '''Create and return a test user'''
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    def tearDown(self):
        models.ProductImage.objects.all().delete()

    def test_register_user_with_email_successful(self):
        '''Test creating a new user with an email'''

        user = create_user()
        self.assertEqual(user.email, 'user@example.com')
        self.assertTrue(user.check_password('test123'))

    @patch('core.models.uuid.uuid4')
    def test_user_file_name_uuid(self, mock_uuid):
        # Test generating image path
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.user_file_name_uuid(None, 'example.jpg')

        self.assertEqual(file_path, f'uploads/accounts/{uuid}.jpg')

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

    def test_create_category(self):
        '''Test creating category'''
        category = models.Category.objects.create(name='test category')
        self.assertEqual(str(category), category.name)

    def test_create_children_category(self):
        '''Test creating children category'''
        c1 = models.Category.objects.create(name='test category1')
        c2 = models.Category.objects.create(name='test category2', parent=c1)
        c3 = models.Category.objects.create(name='test category3', parent=c2)
        self.assertEqual(str(c3), c3.name)
        self.assertEqual(str(c2), c3.parent.name)
        self.assertEqual(str(c1), c3.parent.parent.name)

    def test_create_product(self):
        '''Test creating a product'''
        user = create_user()
        category = models.Category.objects.create(name='test category')
        product = models.Product.objects.create(
            seller=user,
            category=category,
            title='test title',
            price=Decimal('1.00'),
            description='test description',
        )
        self.assertEqual(str(product), product.title)
        self.assertEqual(product.seller, user)

    @patch('core.models.uuid.uuid4')
    def test_create_product_image_with_uuid(self, mock_uuid):
        user = create_user()
        category = models.Category.objects.create(name='test category')
        product = models.Product.objects.create(
            seller=user,
            category=category,
            title='test title',
            price=Decimal('1.00'),
            description='test description',
        )

        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.product_file_name_uuid(None, 'example.jpg')

        product_image = models.ProductImage.objects.create(
            product=product,
            image=file_path
        )
        uuid2 = 'test-uuid2'
        mock_uuid.return_value = uuid2
        file_path2 = models.product_file_name_uuid(None, 'example.jpg')
        product_image2 = models.ProductImage.objects.create(
            product=product,
            image=file_path2
        )
        self.assertEqual(product_image.product, product)
        self.assertEqual(product_image2.product, product)
        self.assertEqual(file_path, product_image.image)
        self.assertEqual(file_path2, product_image2.image)
        self.assertEqual(file_path, f'uploads/products/{uuid}.jpg')
        self.assertEqual(file_path2, f'uploads/products/{uuid2}.jpg')

    def test_create_favorite(self):
        '''Test creating favorite'''
        user = create_user()
        category = models.Category.objects.create(name='test category')
        product = models.Product.objects.create(
            seller=user,
            category=category,
            title='test title',
            price=Decimal('1.00'),
            description='test description',
        )
        favorite = models.Favorite.objects.create(user=user, product=product)
        self.assertEqual(str(favorite), favorite.product.title)

    def test_create_chatroom(self):
        '''Test creating chatroom'''
        seller = create_user()
        buyer = create_user(email='user2@example.com')
        category = models.Category.objects.create(name='test category')
        product = models.Product.objects.create(
            seller=seller,
            category=category,
            title='test title',
            price=Decimal('1.00'),
            description='test description',
        )

        chatroom = models.ChatRoom.objects.create(
            product=product,
            seller=seller,
            buyer=buyer
        )
        self.assertEqual(str(chatroom), chatroom.product.title)

    def test_send_message(self):
        '''Test seding messages to chatroom'''
        seller = get_user_model().objects.create_user(
            email='user@example.com',
            password='test123',
            nickname='testSeller'
        )
        buyer = get_user_model().objects.create_user(
            email='user2@example.com',
            password='test123',
            nickname='testBuyer'
        )
        category = models.Category.objects.create(name='test category')
        product = models.Product.objects.create(
            seller=seller,
            category=category,
            title='test title',
            price=Decimal('1.00'),
            description='test description',
        )

        chatroom = models.ChatRoom.objects.create(
            product=product,
            seller=seller,
            buyer=buyer
        )

        m1 = models.Message.objects.create(
            room=chatroom,
            sender=buyer.nickname,
            text='Hi, I would like to buy this item',
        )

        m2 = models.Message.objects.create(
            room=chatroom,
            sender=seller.nickname,
            text='Hello, sure! how do you want to buy it?',
        )

        self.assertEqual(str(m1), m1.text[:15] + '...')
        self.assertEqual(str(m2), m2.text[:15] + '...')
        self.assertEqual(m1.sender, buyer.nickname)
        self.assertEqual(m2.sender, seller.nickname)

    def test_book_direct_transaction(self):
        '''Test booking a direct transaction from a chat'''
        country = models.Country.objects.create(name='test country')
        county = models.County.objects.create(country=country, name='test country')
        city = models.City.objects.create(county=county, name='test country')
        seller = get_user_model().objects.create_user(
            email='user@example.com',
            password='test123',
            nickname='testSeller'
        )
        buyer = get_user_model().objects.create_user(
            email='user2@example.com',
            password='test123',
            nickname='testBuyer'
        )
        category = models.Category.objects.create(name='test category')
        product = models.Product.objects.create(
            seller=seller,
            category=category,
            title='test title',
            price=Decimal('1.00'),
            description='test description',
        )

        chatroom = models.ChatRoom.objects.create(
            product=product,
            seller=seller,
            buyer=buyer
        )

        json_time = "202402201800"
        time_obj = datetime.strptime(json_time, '%Y%m%d%H%M')
        time_obj = time_obj.replace(tzinfo=timezone.utc)
        transaction = models.DirectTransaction.objects.create(
            chatroom=chatroom,
            location=city,
            location_detail="at Starbucks",
            time=time_obj
        )
        self.assertEqual(str(transaction),
                         f"[S:{chatroom.seller.nickname} B:{chatroom.buyer.nickname}]"
                         f" - {product.title}")

        restored_json_time = transaction.time.strftime('%Y%m%d%H%M')
        self.assertEqual(json_time, restored_json_time)

    def test_create_review(self):
        country = models.Country.objects.create(name='test country')
        county = models.County.objects.create(country=country, name='test country')
        city = models.City.objects.create(county=county, name='test country')
        seller = get_user_model().objects.create_user(
            email='user@example.com',
            password='test123',
            nickname='testSeller'
        )
        buyer = get_user_model().objects.create_user(
            email='user2@example.com',
            password='test123',
            nickname='testBuyer'
        )
        category = models.Category.objects.create(name='test category')
        product = models.Product.objects.create(
            seller=seller,
            category=category,
            title='test title',
            price=Decimal('1.00'),
            description='test description',
        )

        chatroom = models.ChatRoom.objects.create(
            product=product,
            seller=seller,
            buyer=buyer
        )

        json_time = "202402201800"
        time_obj = datetime.strptime(json_time, '%Y%m%d%H%M')
        time_obj = time_obj.replace(tzinfo=timezone.utc)
        transaction = models.DirectTransaction.objects.create(
            chatroom=chatroom,
            location=city,
            location_detail="at Starbucks",
            time=time_obj
        )

        review = models.Review.objects.create(
            transaction=transaction,
            reviewer=buyer,
            receiver=seller,
            review="test review",
            rating=3
        )

        self.assertEqual(str(review),
                         f"[{review.reviewer.nickname} -> {review.receiver.nickname}] "
                         f"{review.transaction.chatroom.product.title}")

        review2 = models.Review.objects.create(
            transaction=transaction,
            reviewer=seller,
            receiver=buyer,
            review="test review",
            rating=3
        )

        self.assertEqual(str(review2),
                         f"[{review2.reviewer.nickname} -> {review2.receiver.nickname}] "
                         f"{review2.transaction.chatroom.product.title}")
        self.assertEqual(review2.transaction.chatroom.product.title, product.title)
