from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from accounts.models import User
from rest_framework import status

""" Tests for Plaid Institution Logo Endpoint """
class InstitutionLogoPlaidViewTestCase(TestCase):
    fixtures = [
        'stocks/tests/fixtures/user.json',
    ]

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.get(id=3)  
        self.client.force_authenticate(self.user)
        self.url = reverse('get_logo')
        self.institution_name = 'Vanguard'

    def test_url(self):
        self.assertEqual(self.url,'/stocks/get_logo/')

    def test_response(self):
        body = {'name': self.institution_name}
        response = self.client.post(self.url, body)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('logo', response.data)

    def test_get_is_not_allowed(self):
        body = {'name': self.institution_name}
        response = self.client.get(self.url, body)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_invalid_access_token(self):
        body = {'name': 'WRONG_INSTITUTION'}
        response = self.client.post(self.url, body)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['Error'], "Institution Does Not Exist")