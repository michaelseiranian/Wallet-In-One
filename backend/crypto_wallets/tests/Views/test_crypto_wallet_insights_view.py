from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from accounts.models import User


class CryptoWalletInsightsTestCase(TestCase):

    fixtures = [
        'accounts/fixtures/user.json',
    ]

    def setUp(self):
        super(TestCase, self).setUp()
        self.client = APIClient()
        self.user = User.objects.get(id=1)
        self.client.force_authenticate(self.user)
        self.url = reverse('crypto_wallet_insights')

    def test_url(self):
        self.assertEqual(self.url, '/crypto_wallets/insights')

    def test_unauthorised(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_insights(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'predicted_balance')
        self.assertContains(response, 'received_spent')
        self.assertContains(response, 'average_spend')
