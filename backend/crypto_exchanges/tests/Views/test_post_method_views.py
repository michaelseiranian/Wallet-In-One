from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from unittest.mock import patch
from crypto_exchanges.serializers import *


class CryptoExchangeAccountCreationTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='test_user', password='password')

    def setUp(self):
        self.client.force_authenticate(user=self.user)

    @patch('crypto_exchanges.services.BinanceFetcher')
    def test_create_binance_account_invalid(self, mock_fetcher):
        url = reverse('binance')
        data = {'api_key': '12345wrongapikeyabcdefghijklmnopqrstuvwxyz', 'secret_key': 'abcdefghijklmnopqrstuvwxyz'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('crypto_exchanges.services.GateioFetcher')
    def test_create_gateio_account_invalid(self, mock_fetcher):
        url = reverse('gateio')
        data = {'api_key': 'zNk5glD4B3owgefu347u9z3s+kHRZ5r/VM46isrhbiGkMFDkl7D/S',
                'secret_key': '48/vZVp234ouitfwIG857AFW5d0vgIM48UgJKfETTl0RPEI3/DWHFi7byVDUSV65tdIQ-='}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'Invalid key provided'})

    @patch('crypto_exchanges.services.CoinListFetcher')
    def test_create_coin_list_account_invalid(self, mock_fetcher):
        url = reverse('coinlist')
        data = {'api_key': 'zNk5glD4B3owgefu347u9z3s+kHRZ5r/VM46isrhbiGkMFDkl7D/S',
                'secret_key': '48/vZVp234ouitfwIG857AFW5d0vgIM48UgJKfETTl0RPEI3/DWHFi7byVDUSV65tdIQ-='}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'invalid api key'})

    @patch('crypto_exchanges.services.CoinBaseFetcher')
    def test_create_coinbase_account_invalid(self, mock_fetcher):
        url = reverse('coinbase')
        data = {'api_key': 'abcdefghijklmnopqrstuvwxyz', 'secret_key': 'abcdefghijklmnopqrstuvwxyz'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'invalid api key'})

    @patch('crypto_exchanges.services.KrakenFetcher')
    def test_create_kraken_account_invalid(self, mock_fetcher):
        url = reverse('kraken')
        data = {'api_key': 'zNk5glD4B3owgefu347u9z3s+kHRZ5r/VM46isrhbiGkMFDkl7D/S',
                'secret_key': '48/vZVp234ouitfwIG857AFW5d0vgIM48UgJKfETTl0RPEI3/DWHFi7byVDUSV65tdIQ-='}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'EAPI:Invalid key'})
