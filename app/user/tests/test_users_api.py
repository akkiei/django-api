from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
# from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**param):
    return get_user_model().objects.create_user(**param)


class PublicUserApiTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_create_valid_user_success(self):
        """ test to create a user successfully """
        payload = {

            'email': 'tester@test.com',
            'password': 'test123',
            'name': 'tester 1'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(**res.data)

        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_already_exist(self):
        """ Test if user already exists or not"""
        payload = {

            'email': 'tester@test.com',
            'password': 'test123',
            'name': 'tester 1'
        }
        # this one create a user
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """ Test if the password is too short ( < 5 )"""

        payload = {

            'email': 'tester@test.com',
            'password': '123',
            'name': 'tester 1'
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(get_user_model().objects.filter(
            email=payload['email']
        ).exists()
                         )

    def test_create_token_for_user(self):
        """ test if token is created for user """
        payload = {

            'email': 'test@london.com',
            'password': 'test123',

        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_token_failed_with_invalid_creds(self):
        """ test fails if creds are wrong"""
        payload = {

            'email': 'test@admin.com',
            'password': 'test123'
        }
        payload_wrong = {

            'email': 'test@admin.com',
            'password': 'na'
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload_wrong)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_token_if_user_does_not_exists(self):
        """ test fails if user doesn't exists"""
        payload = {

            'email': 'test@admin.com',
            'password': 'test123'
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
