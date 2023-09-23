from rest_framework.test import force_authenticate, APIRequestFactory
from django.contrib.auth.models import User
from django.test import TestCase
from unittest.mock import patch
from ...views import get_token_breakdown
from crypto_exchanges.serializers import *


class TestGetTokenBreakdown(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username='@user', first_name='Name', last_name='Lastname',
                                             email='namelastname@example.org')
        self.crypto_exchange_account = CryptoExchangeAccount.objects.create(
            user=self.user,
            crypto_exchange_name='Binance',
            api_key='wfeioguhwe549876y43jh',
            secret_key='wfjbh234987trfhu'
        )

    @patch('crypto_exchanges.views.CurrentMarketPriceFetcher.get_exchange_token_breakdown')
    def test_get_token_breakdown(self, mock_fetcher):
        mock_fetcher.return_value = {
            'token_data': [
                {'x': 'token1', 'y': 1},
                {'x': 'token2', 'y': 2},
            ]
        }

        url = f'crypto-exchanges/get_token_breakdown/{self.crypto_exchange_account.id}/'
        request = self.factory.get(url)
        force_authenticate(request, user=self.user)

        response = get_token_breakdown(request, self.crypto_exchange_account.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'token_data': [{'x': 'token1', 'y': 1}, {'x': 'token2', 'y': 2}]})

    @patch('crypto_exchanges.views.CurrentMarketPriceFetcher.get_exchange_token_breakdown')
    def test_get_token_breakdown_empty_token_data(self, mock_fetcher):
        mock_fetcher.return_value = {
            'token_data': []
        }

        url = f'crypto-exchanges/get_token_breakdown/{self.crypto_exchange_account.id}/'
        request = self.factory.get(url)
        force_authenticate(request, user=self.user)

        response = get_token_breakdown(request, self.crypto_exchange_account.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'token_data': [{'x': 'empty'}]})