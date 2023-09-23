"""Tests for the graph data view."""
from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from rest_framework.test import APIClient, APIRequestFactory
from django.urls import reverse
from accounts.views import graph_data
from accounts.models import User
from banking.models import Account, Transaction
from rest_framework import status
from django.utils import timezone
from banking.tests.helpers import disable_updates
from crypto_wallets.models import CryptoWallet

class GraphDataViewTestCase(TestCase):
    """Tests for the graph data view."""

    fixtures = [
        'accounts/fixtures/user.json',
    ]

    def setUp(self):
        disable_updates()
        self.factory = RequestFactory()
        self.client = APIClient()
        self.url = reverse('graph_data')

    def test_url(self):
        self.assertEqual(self.url,'/graph_data/')

    def test_no_graph_data(self):
        # This user has no accounts connected
        self.user = User.objects.get(id=1)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['all']), 0)

    def test_bank_connected(self):
        # This user has a bank account connected
        self.user = User.objects.get(id=2)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['all']), 1)
        self.assertEqual(response.data['all'][0]['x'], 'Banks')
        self.assertEqual(response.data['all'][0]['y'], 100.00)

    def test_stocks_connected(self):
        # This user has a stock account connected
        self.user = User.objects.get(id=3)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['all']), 1)
        self.assertEqual(response.data['all'][0]['x'], 'Stock Accounts')
        self.assertEqual(response.data['all'][0]['y'], 100.00)

    def test_crypto_exchange_connected(self):
        # This user has a crypto exchange connected
        self.user = User.objects.get(id=5)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['all']), 1)
        self.assertEqual(response.data['all'][0]['x'], 'Cryptocurrency from exchanges')
        self.assertIsInstance(response.data['all'][0]['y'], int)

    def test_crypto_wallet_connected(self):
        # This user has a crypto wallet connected
        self.user = User.objects.get(id=7)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['all']), 1)
        self.assertEqual(response.data['all'][0]['x'], 'Cryptocurrency from wallets')
        self.assertIsInstance(response.data['all'][0]['y'], float)

    def test_bank_and_stock_connected(self):
        # This user has a bank AND stock account connected
        self.user = User.objects.get(id=4)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['all']), 2)
        self.assertEqual(response.data['all'][0]['x'], 'Banks')
        self.assertEqual(response.data['all'][0]['y'], 100.00)
        self.assertEqual(response.data['all'][1]['x'], 'Stock Accounts')
        self.assertEqual(response.data['all'][1]['y'], 100.00)

    def test_bank_and_stock_and_crypto_exchange_connected(self):
        # This user has a bank account AND stock account AND crypto exchange connected
        self.user = User.objects.get(id=6)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['all']), 3)
        self.assertEqual(response.data['all'][0]['x'], 'Banks')
        self.assertEqual(response.data['all'][0]['y'], 100.00)
        self.assertEqual(response.data['all'][1]['x'], 'Stock Accounts')
        self.assertEqual(response.data['all'][1]['y'], 100.00)
        self.assertEqual(response.data['all'][2]['x'], 'Cryptocurrency from exchanges')
        self.assertIsInstance(response.data['all'][2]['y'], int)

    def test_bank_and_stock_and_crypto_exchange_and_crypto_wallet_connected(self):
        # This user has a bank account AND stock account AND crypto exchange AND crypto wallet connected
        self.user = User.objects.get(id=8)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['all']), 4)
        self.assertEqual(response.data['all'][0]['x'], 'Banks')
        self.assertEqual(response.data['all'][0]['y'], 100.00)
        self.assertEqual(response.data['all'][1]['x'], 'Cryptocurrency from wallets')
        self.assertIsInstance(response.data['all'][1]['y'], float)
        self.assertEqual(response.data['all'][2]['x'], 'Stock Accounts')
        self.assertEqual(response.data['all'][2]['y'], 100.00)
        self.assertEqual(response.data['all'][3]['x'], 'Cryptocurrency from exchanges')
        self.assertIsInstance(response.data['all'][3]['y'], int)
