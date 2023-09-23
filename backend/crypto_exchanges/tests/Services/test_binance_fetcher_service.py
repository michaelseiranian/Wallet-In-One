from django.test import TestCase
from unittest.mock import patch, MagicMock, call
from crypto_exchanges.services import *
from datetime import datetime


class TestBinanceFetcher(TestCase):
    def setUp(self):
        self.api_key = "6wfUdme200CGraSbJhIKHc0rssBeiEJHjb8BVUF3jCiskhkgsbVCMvaozeKLQ70N"
        self.secret_key = "Gbjxj44liYPiC5NHHmJwqaCy8b8LAQTi9jlS9SG2H1YktXM5lCjQ3JVTt7Br1DfC"
        self.fetcher = BinanceFetcher(api_key=self.api_key, secret_key=self.secret_key)

    def tearDown(self):
        patch.stopall()

    def test_init(self):
        self.assertEquals(self.fetcher.api_key, self.api_key)
        self.assertEquals(self.fetcher.secret_key, self.secret_key)
        self.assertEqual(self.fetcher.symbols, ['BTCUSDT', 'ETHUSDT', 'ADAUSDT', 'XRPUSDT', 'SOLUSDT'])

    def test_signature(self):
        params = {}
        query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
        expexted_value = hmac.new(self.secret_key.encode('utf-8'), query_string.encode('utf-8'), sha256).hexdigest()
        self.assertEquals(self.fetcher.signature({}), expexted_value)

    @patch('requests.get')
    def test_get_account_data(self, mock_get):
        # Test that the method sends a GET request with the correct parameters
        mock_response = MagicMock()
        mock_response.json.return_value = {'test': 'data'}
        mock_get.return_value = mock_response

        expected_headers = {'X-MBX-APIKEY': self.api_key}
        expected_timestamp = str(self.fetcher.get_current_time())
        expected_signature = self.fetcher.hash(timestamp=f"timestamp={expected_timestamp}")
        expected_url = f"https://api.binance.com/api/v3/account?timestamp={expected_timestamp}" \
                       f"&signature={expected_signature}"

        self.fetcher.get_account_data(f"timestamp={expected_timestamp}")

        mock_get.assert_called_with(url=expected_url, headers=expected_headers)

    @patch('requests.get')
    def test_get_trading_history(self, mock_get):
        class MockResponse:
            def __init__(self, status_code, json_data):
                self.status_code = status_code
                self.json_data = json_data

            def json(self):
                return self.json_data

        expected_headers = {'X-MBX-APIKEY': self.fetcher.api_key}
        expected_timestamp = self.fetcher.get_current_time()
        expected_params_btcusdt = {'symbol': 'BTCUSDT', 'timestamp': expected_timestamp}
        expected_params_ethusdt = {'symbol': 'ETHUSDT', 'timestamp': expected_timestamp}
        expected_params_adausdt = {'symbol': 'ADAUSDT', 'timestamp': expected_timestamp}
        expected_params_xrpusdt = {'symbol': 'XRPUSDT', 'timestamp': expected_timestamp}
        expected_params_solusdt = {'symbol': 'SOLUSDT', 'timestamp': expected_timestamp}
        expected_signature_btcusdt = self.fetcher.signature(expected_params_btcusdt)
        expected_signature_ethusdt = self.fetcher.signature(expected_params_ethusdt)
        expected_signature_adausdt = self.fetcher.signature(expected_params_adausdt)
        expected_signature_xrpusdt = self.fetcher.signature(expected_params_xrpusdt)
        expected_signature_solusdt = self.fetcher.signature(expected_params_solusdt)

        btcusdt_response = [{'symbol': 'BTCUSDT', 'price': '10000', 'qty': '0.5', 'commission': '0.0005'}]
        ethusdt_response = [{'symbol': 'ETHUSDT', 'price': '3000', 'qty': '1', 'commission': '0.001'}]
        adausdt_response = [{'symbol': 'ADAUSDT', 'price': '2', 'qty': '100', 'commission': '0.01'}]
        xrpusdt_response = [{'symbol': 'XRPUSDT', 'price': '1', 'qty': '200', 'commission': '0.02'}]
        solusdt_response = [{'symbol': 'SOLUSDT', 'price': '150', 'qty': '2', 'commission': '0.003'}]

        mock_get.side_effect = [
            MockResponse(status_code=200, json_data=btcusdt_response),
            MockResponse(status_code=200, json_data=ethusdt_response),
            MockResponse(status_code=200, json_data=adausdt_response),
            MockResponse(status_code=200, json_data=xrpusdt_response),
            MockResponse(status_code=200, json_data=solusdt_response)
        ]

        actual_response = self.fetcher.get_trading_history(expected_timestamp)

        expected_response = {
            'BTCUSDT': btcusdt_response,
            'ETHUSDT': ethusdt_response,
            'ADAUSDT': adausdt_response,
            'XRPUSDT': xrpusdt_response,
            'SOLUSDT': solusdt_response
        }

        assert actual_response == expected_response

        mock_get.assert_has_calls([
            call('https://api.binance.com/api/v3/myTrades', headers=expected_headers,
                 params={**expected_params_btcusdt, **{'signature': expected_signature_btcusdt}}),
            call('https://api.binance.com/api/v3/myTrades', headers=expected_headers,
                 params={**expected_params_ethusdt, **{'signature': expected_signature_ethusdt}}),
            call('https://api.binance.com/api/v3/myTrades', headers=expected_headers,
                 params={**expected_params_adausdt, **{'signature': expected_signature_adausdt}}),
            call('https://api.binance.com/api/v3/myTrades', headers=expected_headers,
                 params={**expected_params_xrpusdt, **{'signature': expected_signature_xrpusdt}}),
            call('https://api.binance.com/api/v3/myTrades', headers=expected_headers,
                 params={**expected_params_solusdt, **{'signature': expected_signature_solusdt}}),
        ])

    @patch('crypto_exchanges.services.ExchangeFetcher.get_current_time')
    def test_get_trading_history_no_timestamp(self, mock_get_current_time):
        mock_get_current_time.return_value = datetime(2022, 3, 22, 12, 0, 0)

        result = self.fetcher.get_trading_history()

        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 5)
