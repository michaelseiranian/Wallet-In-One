from datetime import datetime
from django.http import HttpResponse, HttpRequest
from rest_framework.test import force_authenticate, APIClient
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from unittest.mock import patch
from ...views import GenericCryptoExchanges, BinanceView, GateioView, CoinListView, CoinBaseView, KrakenView
from crypto_exchanges.serializers import *
from collections import OrderedDict
import json


def convert_date_string(date_string):
    dt = datetime.fromisoformat(date_string)
    return dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ')


class GetMethodsOfViewsTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.url = reverse('crypto-exchanges')

    def test_get_crypto_exchange_accounts(self):
        account = CryptoExchangeAccount.objects.create(
            user=self.user,
            api_key='my_api_key',
            secret_key='my_secret_key',
            crypto_exchange_name='binance',
        )

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = [OrderedDict([('crypto_exchange_name', 'binance'), ('api_key', 'my_api_key'),
                                      ('secret_key', 'my_secret_key'),
                                      ('created_at', convert_date_string(str(account.created_at))), ('id', 1)])]
        self.assertEqual(response.data, expected_data)

    @patch.object(GenericCryptoExchanges, 'get')
    def test_binance_view_get(self, mock_get):
        mock_response_data = {'key': 'value'}
        mock_response = HttpResponse(json.dumps(mock_response_data), content_type='application/json', status=200)
        mock_get.return_value = mock_response

        request = HttpRequest()
        request.method = 'GET'
        request.headers = {'Accept': 'application/json'}

        force_authenticate(request, user=self.user)

        view = BinanceView.as_view()

        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content.decode('utf-8'), json.dumps(mock_response_data))

    @patch.object(GenericCryptoExchanges, 'get')
    def test_gateio_view_get(self, mock_get):
        mock_response_data = {'key': 'value'}
        mock_response = HttpResponse(json.dumps(mock_response_data), content_type='application/json', status=200)
        mock_get.return_value = mock_response

        request = HttpRequest()
        request.method = 'GET'
        request.headers = {'Accept': 'application/json'}

        force_authenticate(request, user=self.user)

        view = GateioView.as_view()

        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content.decode('utf-8'), json.dumps(mock_response_data))

    @patch.object(GenericCryptoExchanges, 'get')
    def test_coinlist_view_get(self, mock_get):
        mock_response_data = {'key': 'value'}
        mock_response = HttpResponse(json.dumps(mock_response_data), content_type='application/json', status=200)
        mock_get.return_value = mock_response

        request = HttpRequest()
        request.method = 'GET'
        request.headers = {'Accept': 'application/json'}

        force_authenticate(request, user=self.user)

        view = CoinListView.as_view()

        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content.decode('utf-8'), json.dumps(mock_response_data))

    @patch.object(GenericCryptoExchanges, 'get')
    def test_coinbase_view_get(self, mock_get):
        mock_response_data = {'key': 'value'}
        mock_response = HttpResponse(json.dumps(mock_response_data), content_type='application/json', status=200)
        mock_get.return_value = mock_response

        request = HttpRequest()
        request.method = 'GET'
        request.headers = {'Accept': 'application/json'}

        force_authenticate(request, user=self.user)

        view = CoinBaseView.as_view()

        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content.decode('utf-8'), json.dumps(mock_response_data))

    @patch.object(GenericCryptoExchanges, 'get')
    def test_kraken_view_get(self, mock_get):
        mock_response_data = {'key': 'value'}
        mock_response = HttpResponse(json.dumps(mock_response_data), content_type='application/json', status=200)
        mock_get.return_value = mock_response

        request = HttpRequest()
        request.method = 'GET'
        request.headers = {'Accept': 'application/json'}

        force_authenticate(request, user=self.user)

        view = KrakenView.as_view()

        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content.decode('utf-8'), json.dumps(mock_response_data))
