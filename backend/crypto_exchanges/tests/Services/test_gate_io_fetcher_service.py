from django.test import TestCase
from unittest.mock import patch, MagicMock
from crypto_exchanges.services import *


class TestGateioFetcher(TestCase):
    def setUp(self):
        self.api_key = "4772671c2cdbd350015a07a27a80f466"
        self.secret_key = "8fa1cc672fc070ead7d1ed4428d1caf454b37248ada8d93e13ccf3f52e7e01fa"
        self.fetcher = GateioFetcher(api_key=self.api_key, secret_key=self.secret_key)
        self.mock_signature = patch('crypto_exchanges.services.GateioFetcher.signature').start()
        self.mock_signature.return_value = {'KEY': self.api_key, 'Timestamp': '123', 'SIGN': 'abc'}

    def tearDown(self):
        patch.stopall()

    def test_init(self):
        self.assertEquals(self.fetcher.api_key, self.api_key)
        self.assertEquals(self.fetcher.secret_key, self.secret_key)
        self.assertEqual(self.fetcher.symbols, ['BTC_USDT', 'ETH_USDT', 'ADA_USDT', 'XRP_USDT', 'SOL_USDT', 'ARV_USDT'])
        self.assertEquals(self.fetcher.host, 'https://api.gateio.ws')
        self.assertEquals(self.fetcher.prefix, '/api/v4')
        self.assertEquals(self.fetcher.headers, {'Accept': 'application/json', 'Content-Type': 'application/json'})

    def test_signature(self):
        self.tearDown()

        method = 'GET'
        url = 'v1'
        query_string = None
        payload_string = None
        timestamp = str(time.time())
        message = sha512()
        message.update((payload_string or "").encode('utf-8'))
        hashed_payload = message.hexdigest()
        path = '%s\n%s\n%s\n%s\n%s' % (method, url, query_string or "", hashed_payload, timestamp)
        signature = hmac.new(self.secret_key.encode('utf-8'), path.encode('utf-8'), sha512).hexdigest()

        expected_result = {'KEY': self.api_key, 'Timestamp': timestamp, 'SIGN': signature}
        actual_result = self.fetcher.signature(method, url, None, None, timestamp=timestamp)

        self.assertEquals(actual_result, expected_result)

    @patch('requests.get')
    def test_get_account_data(self, mock_get):
        mock_signature = self.mock_signature
        expected_result = {'result': 'success'}
        mock_signature.return_value = {'KEY': self.api_key, 'Timestamp': '123', 'SIGN': 'abc'}
        mock_get.return_value = MagicMock(status_code=200, json=MagicMock(return_value=expected_result))

        result = self.fetcher.get_account_data()

        mock_signature.assert_called_once_with('GET', self.fetcher.prefix + '/spot/accounts', '')
        mock_get.assert_called_once_with(self.fetcher.host + self.fetcher.prefix + '/spot/accounts',
                                         headers={'Accept': 'application/json', 'Content-Type': 'application/json',
                                                  'KEY': self.api_key, 'Timestamp': '123', 'SIGN': 'abc'})
        self.assertEqual(result, expected_result)

    def test_get_trading_history_types(self):
        # Call the get_trading_history method
        result = self.fetcher.get_trading_history()

        # Assert that the result is a dictionary with keys matching the symbols in the symbols list
        self.assertIsInstance(result, dict)
        self.assertCountEqual(result.keys(), self.fetcher.symbols)

        # Assert that the values in the dictionary are non-empty lists
        for symbol, trades in result.items():
            self.assertIsInstance(trades, list)
            self.assertTrue(trades)

    @patch('requests.get')
    def test_get_trading_history(self, mock_get):
        expected_result = {
            'BTC_USDT': {'result': 'success'},
            'ETH_USDT': {'result': 'success'},
            'ADA_USDT': {'result': 'success'},
            'XRP_USDT': {'result': 'success'},
            'SOL_USDT': {'result': 'success'},
            'ARV_USDT': {'result': 'success'},
        }
        mock_signature = self.mock_signature
        mock_signature.return_value = {'KEY': self.api_key, 'Timestamp': '123', 'SIGN': 'abc'}
        mock_get.return_value = MagicMock(status_code=200, json=MagicMock(return_value={'result': 'success'}))

        result = self.fetcher.get_trading_history()

        mock_signature.assert_any_call('GET', self.fetcher.prefix + '/spot/trades?currency_pair=BTC_USDT&limit=10')
        mock_signature.assert_any_call('GET', self.fetcher.prefix + '/spot/trades?currency_pair=ETH_USDT&limit=10')
        mock_signature.assert_any_call('GET', self.fetcher.prefix + '/spot/trades?currency_pair=ADA_USDT&limit=10')
        mock_signature.assert_any_call('GET', self.fetcher.prefix + '/spot/trades?currency_pair=XRP_USDT&limit=10')
        mock_signature.assert_any_call('GET', self.fetcher.prefix + '/spot/trades?currency_pair=SOL_USDT&limit=10')
        mock_signature.assert_any_call('GET', self.fetcher.prefix + '/spot/trades?currency_pair=ARV_USDT&limit=10')
        assert mock_signature.call_count == 6

        mock_get.assert_any_call(
            self.fetcher.host + self.fetcher.prefix + '/spot/trades?currency_pair=BTC_USDT&limit=10',
            headers={'Accept': 'application/json', 'Content-Type': 'application/json', 'KEY': self.api_key,
                     'Timestamp': '123', 'SIGN': 'abc'})
        mock_get.assert_any_call(
            self.fetcher.host + self.fetcher.prefix + '/spot/trades?currency_pair=ETH_USDT&limit=10',
            headers={'Accept': 'application/json', 'Content-Type': 'application/json', 'KEY': self.api_key,
                     'Timestamp': '123', 'SIGN': 'abc'})
        mock_get.assert_any_call(
            self.fetcher.host + self.fetcher.prefix + '/spot/trades?currency_pair=ADA_USDT&limit=10',
            headers={'Accept': 'application/json', 'Content-Type': 'application/json', 'KEY': self.api_key,
                     'Timestamp': '123', 'SIGN': 'abc'})
        mock_get.assert_any_call(
            self.fetcher.host + self.fetcher.prefix + '/spot/trades?currency_pair=XRP_USDT&limit=10',
            headers={'Accept': 'application/json', 'Content-Type': 'application/json', 'KEY': self.api_key,
                     'Timestamp': '123', 'SIGN': 'abc'})
        mock_get.assert_any_call(
            self.fetcher.host + self.fetcher.prefix + '/spot/trades?currency_pair=SOL_USDT&limit=10',
            headers={'Accept': 'application/json', 'Content-Type': 'application/json', 'KEY': self.api_key,
                     'Timestamp': '123', 'SIGN': 'abc'})
        mock_get.assert_any_call(
            self.fetcher.host + self.fetcher.prefix + '/spot/trades?currency_pair=ARV_USDT&limit=10',
            headers={'Accept': 'application/json', 'Content-Type': 'application/json', 'KEY': self.api_key,
                     'Timestamp': '123', 'SIGN': 'abc'})

