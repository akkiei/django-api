from django.test import TestCase
from django.contrib.auth import get_user_model


class ModalTests(TestCase):

    def test_create_user_with_email_pass(self):
        """ Test user creation with email pass"""

        email = "dummy@dumdum.com"
        password = "qwerty"

        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_create_user(self):
        email = "dummy@dumdum.com"
        password = "qwerty"

        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_user_with_no_email(self):
        password = "qwerty"

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                None, password=password
            )

    def test_is_superuser(self):
        user = get_user_model().objects.create_super_user(
            "dummy@gmail.com",
            "test1234"
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
