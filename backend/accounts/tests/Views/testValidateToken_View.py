"""Tests for the token validation"""
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from django.urls import reverse
from accounts.views import validate_token
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ErrorDetail
from accounts.models import User
from rest_framework.authtoken.models import Token

class ValidateTokenTests(APITestCase):
    """Tests for the token validation"""

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass'
        )
        self.token = Token.objects.create(user=self.user)
        self.request = self.factory.get(reverse('validate_token'))

    def test_valid_token(self):
        self.request.META['HTTP_AUTHORIZATION'] = f'Token {self.token.key}'
        response = validate_token(self.request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'token_valid': True})

    def test_invalid_token(self):
        self.request.META['HTTP_AUTHORIZATION'] = 'Token invalid_token'
        response = validate_token(self.request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {'detail': ErrorDetail(string='Invalid token.', code='authentication_failed')})

    def test_token_invalid_if_user_deleted(self):
        self.request.META['HTTP_AUTHORIZATION'] = f'Token {self.token.key}'
        self.user.delete()
        response = validate_token(self.request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {'detail': ErrorDetail(string='Invalid token.', code='authentication_failed')})


    def test_missing_token(self):
        response = validate_token(self.request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {'detail': ErrorDetail(string='Authentication credentials were not provided.', code='not_authenticated')})