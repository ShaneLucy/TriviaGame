from django.test import TestCase
from django.contrib.auth import get_user_model
from Database.models import *
from django.db import IntegrityError, transaction


def sample_user(username='Headshotzz', email='arealmail@gmail.com',
                password='password123'):
    return get_user_model().objects.create_user(username, email, password)


class CustomUserModelTests(TestCase):
    """Tests to be performed on models"""

    def setUp(self):
        self.username = 'Somerandom'
        self.email = 'definitelynot@gmail.com'
        self.password = 'password123'

    def test_create_user(self):
        """Test that a user will be created when valid
        credentials are provided"""
        user = get_user_model().objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password
        )

        self.assertEqual(user.email, self.email)
        self.assertTrue(user.check_password(self.password))
        self.assertEqual(get_user_model().objects.count(), 1)

    def test_create_user_without_email(self):
        """Test that a user won't be created without an email address"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                username=self.username,
                email=None,
                password=self.password
            )

    def test_create_user_without_username(self):
        """Test that a user won't be created without a username"""
        try:
            with transaction.atomic():
                get_user_model().objects.create_user(
                    username=None,
                    email=self.email,
                    password=self.password
                )
        except IntegrityError:
            pass

        self.assertEqual(get_user_model().objects.count(), 0)

    def test_duplicate_email(self):
        """Test that a user won't be created with a duplicated email"""
        get_user_model().objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password
        )

        try:
            with transaction.atomic():
                get_user_model().objects.create_user(
                    username='AnotherRandom',
                    email=self.email,
                    password=self.password
                )
        except IntegrityError:
            pass

        self.assertEqual(get_user_model().objects.count(), 1)

    def test_duplicate_username(self):
        """Test that a user won't be created with a duplicated username"""
        get_user_model().objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password
        )

        try:
            with transaction.atomic():
                get_user_model().objects.create_user(
                    username=self.username,
                    email='different@protonmail.com',
                    password=self.password
                )
        except IntegrityError:
            pass

        self.assertEqual(get_user_model().objects.count(), 1)

    def test_email_is_normalised(self):
        """Test that emails are normalised"""
        email = 'fakemail@PROTONMAIL.com'
        get_user_model().objects.create_user(
            username=self.username,
            email=email
        )

        self.assertEqual(get_user_model().objects.get().email, email.lower())

    def test_create_superuser(self):
        """Test the creation of a superuser"""
        user = get_user_model().objects.create_superuser(
            username=self.username,
            email=self.email,
            password=self.password
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_delete_user(self):
        """Test that a users account can be deleted"""
        get_user_model().objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password
        )

        self.assertEqual(get_user_model().objects.count(), 1)

        deleted_user = get_user_model().objects.get()
        deleted_user.delete()

        self.assertEqual(get_user_model().objects.count(), 0)

    def test_delete_superuser(self):
        """Test that a superuser can be deleted"""
        get_user_model().objects.create_superuser(
            username=self.username,
            email=self.email,
            password=self.password
        )
        self.assertEqual(get_user_model().objects.count(), 1)

        deleted_user = get_user_model().objects.get()
        deleted_user.delete()

        self.assertEqual(get_user_model().objects.count(), 0)

    def test_username_is_returned(self):
        """Test that a users username is returned as the objects
        string reprsentation instead of the email address"""
        user = get_user_model().objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password
        )

        self.assertEqual(str(user), self.username)
