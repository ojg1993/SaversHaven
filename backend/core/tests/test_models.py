from django.contrib.auth import get_user_model
from django.test import TestCase


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
