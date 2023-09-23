from django.test import TestCase
from unittest.mock import patch, MagicMock, ANY, call
from crypto_exchanges.services import *


class TestCoinListFetcher(TestCase):
    def setUp(self):
        self.api_key = "3ad7fce8-815b-4371-8671-95571c1c7666"
        self.secret_key = "q6onPwTnucwK6YWbK3JWa5fyQ7G46uP5ef2uoTLJ4vo+urPapDwbtvzY4UNhJjieE+0a3+K9gN7vFXtPIkFUhg=="
        self.fetcher = CoinListFetcher(api_key=self.api_key, secret_key=self.secret_key)

    def tearDown(self):
        patch.stopall()

    def test_init(self):
        self.assertEquals(self.fetcher.api_key, self.api_key)
        self.assertEquals(self.fetcher.secret_key, self.secret_key)

    def test_signature(self):
        timestamp = str(int(time.time()))
        path = '/v1/accounts/'
        method = 'GET'
        body = None

        data = self.fetcher.prehash(timestamp, method, path, body)
        key = b64decode(self.secret_key)

        hmc = hmac.new(key, data.encode('utf-8'), digestmod=sha256)
        expected_result = b64encode(hmc.digest()).decode('utf-8')

        self.assertEquals(self.fetcher.signature(data, key), expected_result)

    @patch('requests.get')
    def test_get_account_data(self, mock_get):

        mock_response = MagicMock()
        mock_response.json.return_value = {"accounts": [{"trader_id": "1234"}, {"trader_id": "5678"}]}
        mock_get.return_value = mock_response


        result = self.fetcher.get_account_data()
        self.assertEqual(len(result), 1)


        mock_get.assert_any_call(
            url="https://trade-api.coinlist.co/v1/accounts/",
            headers={
                'Content-Type': 'application/json',
                'CL-ACCESS-KEY': self.api_key,
                'CL-ACCESS-SIG': ANY,
                'CL-ACCESS-TIMESTAMP': ANY
            }
        )


        self.assertEqual(result, {'accounts': [{'trader_id': '1234'}, {'trader_id': '5678'}]})

    def test_get_trading_history_types(self):

        result = self.fetcher.get_trading_history()


        self.assertIsInstance(result, dict)


        for symbol, trades in result.items():
            self.assertIsInstance(trades, list)
            self.assertTrue(trades)

    @patch('requests.get')
    def test_get_trading_history(self, mock_get):

        mock_response = MagicMock()
        mock_response.json.return_value = [
            {'symbol': 'BTC', 'amount': '1.00000000', 'type': 'deposit'},
            {'symbol': 'ETH', 'amount': '2.00000000', 'type': 'withdrawal'}
        ]
        mock_get.return_value = mock_response

        result = self.fetcher.get_trading_history()
        self.assertEqual(len(result), 2)

    @patch('requests.get')
    def test_get_trading_history2(self, mock_get):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.status_code = status_code
                self.json_data = json_data

            def json(self):
                return self.json_data

        mock_get.side_effect = [

            MockResponse({
                'accounts': [
                    {'trader_id': '123'},
                    {'trader_id': '456'}
                ]
            }, 200),

            MockResponse({
                'history': [
                    {'id': '123-1', 'timestamp': ANY, 'amount': '10.0', 'currency': 'BTC'},
                ]
            }, 200),

            MockResponse({
                'history': [
                    {'id': '456-1', 'timestamp': ANY, 'amount': '100.0', 'currency': 'BTC'}
                ]
            }, 200)
        ]


        trading_history = self.fetcher.get_trading_history()

        expected_result = {
            'history': [
                {
                    'id': '456-1',
                    'timestamp': ANY,
                    'amount': '100.0',
                    'currency': 'BTC'
                },
            ]
        }

        self.assertEqual(trading_history, expected_result)

        mock_get.assert_has_calls([
            call(url='https://trade-api.coinlist.co/v1/accounts/', headers=ANY),
            call(url='https://trade-api.coinlist.co/v1/accounts/123/ledger', headers=ANY),
            call(url='https://trade-api.coinlist.co/v1/accounts/456/ledger', headers=ANY)
        ])
