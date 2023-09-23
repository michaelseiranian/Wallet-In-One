from rest_framework.test import force_authenticate
from rest_framework.test import APITestCase, APIRequestFactory
from django.contrib.auth.models import User
from rest_framework import status
from unittest.mock import patch
from ...views import get_exchange_balances
from crypto_exchanges.serializers import *


class GetExchangeBalancesTestCase(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.crypto_exchange_account = CryptoExchangeAccount.objects.create(
            user=self.user,
            crypto_exchange_name='Binance',
            api_key='wfeioguhwe549876y43jh',
            secret_key='wfjbh234987trfhu'
        )

    def test_get_exchange_balances_success(self):
        url = 'crypto-exchanges/get_exchange_balances/'
        request = self.factory.get(url)
        force_authenticate(request, user=self.user)

        with patch('crypto_exchanges.views.CurrentMarketPriceFetcher') as fetcher_mock:
            fetcher_instance_mock = fetcher_mock.return_value
            fetcher_instance_mock.chart_breakdown_crypto_exchanges.return_value = {
                'balances': [{'exchange': 'Test Exchange', 'btc_value': 1.0}]}
            response = get_exchange_balances(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'balances': [{'exchange': 'Test Exchange', 'btc_value': 1.0}]})

    def test_get_exchange_balances_failure_unauthenticated(self):
        CryptoExchangeAccount.objects.filter(user=self.user).delete()
        url = 'crypto-exchanges/get_exchange_balances/'
        request = self.factory.get(url)
        response = get_exchange_balances(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_exchange_balances_failure_no_exchanges(self):
        CryptoExchangeAccount.objects.filter(user=self.user).delete()

        url = 'crypto-exchanges/get_exchange_balances/'
        request = self.factory.get(url)
        force_authenticate(request, user=self.user)

        response = get_exchange_balances(request)
        self.assertEqual(response.data, None)

