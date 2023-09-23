from django.test import TestCase
from unittest.mock import patch, MagicMock
from crypto_exchanges.services import *


class TestCoinBaseFetcher(TestCase):
    def setUp(self):
        self.api_key = "Lt4fELfkTX1Oif0y"
        self.secret_key = "Jt2nHesybO3Wx8pgWUXlxr3hHZiqgDKu"
        self.fetcher = CoinBaseFetcher(api_key=self.api_key, secret_key=self.secret_key)

    def tearDown(self):
        patch.stopall()

    def test_init(self):
        self.assertEquals(self.fetcher.api_key, self.api_key)
        self.assertEquals(self.fetcher.secret_key, self.secret_key.encode('utf-8'))

    def test_call_method(self):
        request = MagicMock()
        request.method = 'GET'
        request.path_url = '/v1/accounts/'
        request.body = None
        request.headers = {}

        instance = CoinBaseFetcher(self.api_key, self.secret_key)

        response = instance(request)

        expected_signature = instance.signature(str(int(time.time())) + request.method + request.path_url)
        self.assertEqual(request.headers['CB-ACCESS-SIGN'], expected_signature)
        self.assertEqual(request.headers['CB-ACCESS-TIMESTAMP'], str(int(time.time())))
        self.assertEqual(request.headers['CB-ACCESS-KEY'], self.api_key)

    def test_signature(self):
        message = str(int(time.time())) + 'GET' + 'v1/accounts' + ''
        expected_result = hmac.new(self.secret_key.encode('utf-8'), message.encode(), sha256).hexdigest()

        self.assertEquals(self.fetcher.signature(message), expected_result)

    @patch('requests.get')
    def test_get_account_data(self, mock_get):
        # Set up mock response from Coinbase API
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'data': [
                {
                    'balance': '100.0',
                    'currency': 'BTC',
                },
                {
                    'balance': '200.0',
                    'currency': 'ETH',
                },
            ]
        }
        mock_get.return_value = mock_response

        account_data = self.fetcher.get_account_data()

        mock_get.assert_called_once_with(
            'https://api.coinbase.com/v2/accounts',
            auth=self.fetcher
        )

        self.assertEqual(account_data, ['100.0', '200.0'])

    @patch('requests.get')
    def test_get_trading_history(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'data': [
                {
                    'id': '123',
                    'product_id': 'BTC-USD',
                    'size': '1.0',
                    'price': '50000.0',
                    'side': 'buy',
                },
                {
                    'id': '456',
                    'product_id': 'ETH-USD',
                    'size': '2.0',
                    'price': '2000.0',
                    'side': 'sell',
                },
            ]
        }
        mock_get.return_value = mock_response

        trading_history = self.fetcher.get_trading_history()

        mock_get.assert_called_once_with(
            'https://api.coinbase.com/api/v3/brokerage/orders/historical/fills',
            auth=self.fetcher,
        )


        self.assertEqual(trading_history['data'][0]['id'], '123')
        self.assertEqual(trading_history['data'][0]['product_id'], 'BTC-USD')
        self.assertEqual(trading_history['data'][0]['size'], '1.0')
        self.assertEqual(trading_history['data'][0]['price'], '50000.0')
        self.assertEqual(trading_history['data'][0]['side'], 'buy')

        self.assertEqual(trading_history['data'][1]['id'], '456')
        self.assertEqual(trading_history['data'][1]['product_id'], 'ETH-USD')
        self.assertEqual(trading_history['data'][1]['size'], '2.0')
        self.assertEqual(trading_history['data'][1]['price'], '2000.0')
        self.assertEqual(trading_history['data'][1]['side'], 'sell')
