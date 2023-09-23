from unittest.mock import patch
from accounts.models import User
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from crypto_exchanges.models import CryptoExchangeAccount


class UpdateAllTokensTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='testuser')
        self.url = reverse('update')
        self.client.force_authenticate(user=self.user)
        self.binance_account = CryptoExchangeAccount.objects.create(user=self.user, crypto_exchange_name='Binance', api_key='binance_api_key', secret_key='binance_secret_key')
        self.gateio_account = CryptoExchangeAccount.objects.create(user=self.user, crypto_exchange_name='GateIo', api_key='gateio_api_key', secret_key='gateio_secret_key1')
        self.coinlist_account = CryptoExchangeAccount.objects.create(user=self.user, crypto_exchange_name='CoinList',
                                                                   api_key='coinlist_api_keyr4',
                                                                   secret_key='coinlist_secret_keygfr')
        self.coinbase_account = CryptoExchangeAccount.objects.create(user=self.user, crypto_exchange_name='CoinBase',
                                                                   api_key='coinbase_api_key',
                                                                   secret_key='coinbase_secret_key')
        self.kraken_account = CryptoExchangeAccount.objects.create(user=self.user, crypto_exchange_name='Kraken',
                                                                   api_key='kraken_api_key',
                                                                   secret_key='kraken_secret_key1')

    def test_update_all_tokens_success(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Success. Data was updated successfully')
        self.assertFalse(CryptoExchangeAccount.objects.filter(user=self.user).exists())

    def test_update_all_tokens_api_view_called(self):
        with patch('crypto_exchanges.views.BinanceView.post') as binance_mock, \
             patch('crypto_exchanges.views.GateioView.post') as gateio_mock, \
             patch('crypto_exchanges.views.CoinListView.post') as coinlist_mock, \
             patch('crypto_exchanges.views.CoinBaseView.post') as coinbase_mock, \
             patch('crypto_exchanges.views.KrakenView.post') as kraken_mock:
            response = self.client.post(self.url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            binance_mock.assert_called_once()
            gateio_mock.assert_called_once()
            coinlist_mock.assert_called_once()
            coinbase_mock.assert_called_once()
            kraken_mock.assert_called_once()

    def test_update_all_tokens_no_accounts(self):
        CryptoExchangeAccount.objects.all().delete()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Success. Data was updated successfully')
        self.assertFalse(CryptoExchangeAccount.objects.filter(user=self.user).exists())
