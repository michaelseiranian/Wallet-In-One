from django.test import TestCase, Client
from rest_framework.test import APIClient
from django.urls import reverse
from accounts.models import User
from rest_framework import status
from plaid.model.link_token_get_request import LinkTokenGetRequest
from stocks.services import setUpClient
from plaid.model.country_code import CountryCode
from plaid.model.products import Products

""" Tests for Plaid Link Token Endpoint """
class InitiatePlaidLinkTestCase(TestCase):
    
    fixtures = [
        'stocks/tests/fixtures/user.json',
    ]

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.get(id=3)
        self.client.force_authenticate(self.user)
        self.url = reverse('initiate_plaid_link')

    def test_url(self):
        self.assertEqual(self.url,'/stocks/initiate_plaid_link/')

    def test_response(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('link_token', response.data)
        self.assertIsNotNone(response.data['link_token'])

    def test_get_is_not_allowed(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_link_token(self):
        client = setUpClient()
        response = self.client.post(self.url)
        link_token = response.data['link_token']
        link_token_info = client.link_token_get(LinkTokenGetRequest(link_token))
        self.assertEqual(link_token, link_token_info['link_token'])
        self.assertIsNotNone(link_token_info['expiration'])
        self.assertIsNotNone(link_token_info['created_at'])
        self.assertIsNotNone(link_token_info['metadata'])
        self.assertEqual(link_token_info['metadata']['client_name'], 'KCL')
        self.assertEqual(link_token_info['metadata']['country_codes'], [CountryCode("US")])
        self.assertEqual(link_token_info['metadata']['initial_products'], [Products("investments"), Products("transactions")])
        self.assertEqual(link_token_info['metadata']['language'], 'en')
    
