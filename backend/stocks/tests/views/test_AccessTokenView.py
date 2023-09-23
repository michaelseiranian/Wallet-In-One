from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from accounts.models import User
from rest_framework import status
from stocks.services import setUpClient
from plaid.model.sandbox_public_token_create_request import SandboxPublicTokenCreateRequest
from plaid.model.products import Products

""" Tests for Plaid Access Token Endpoint """
class AccessTokenTestCase(TestCase):

    fixtures = [
        'stocks/tests/fixtures/user.json',
    ]

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.get(id=3)  
        self.client.force_authenticate(self.user)
        self.url = reverse('get_access_token')
        self.public_token = self.get_public_token()

    def get_public_token(self):
        client = setUpClient()
        public_token = client.sandbox_public_token_create(SandboxPublicTokenCreateRequest(institution_id="ins_109512", initial_products=[Products("investments")]))
        return public_token['public_token']

    def test_url(self):
        self.assertEqual(self.url,'/stocks/get_access_token/')

    def test_response(self):
        body = {'public_token': self.public_token}
        response = self.client.post(self.url, body)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.data)
        self.assertIsNotNone(response.data['access_token'])

    def test_get_is_not_allowed(self):
        body = {'public_token': self.public_token}
        response = self.client.get(self.url, body)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_invalid_public_token(self):
        body = {'public_token': 'WRONG_PUBLIC_TOKEN'}
        response = self.client.post(self.url, body)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['Error']['error_code'], "INVALID_PUBLIC_TOKEN")

        