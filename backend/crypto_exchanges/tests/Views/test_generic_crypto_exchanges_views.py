from rest_framework.response import Response
import unittest
from ...views import GenericCryptoExchanges, BinanceView, GateioView, CoinListView, CoinBaseView, KrakenView
from ...services import BinanceFetcher, GateioFetcher, CoinListFetcher, CoinBaseFetcher, KrakenFetcher


class TestGenericCryptoExchanges(unittest.TestCase):
    def test_init(self):
        crypto_exchange = GenericCryptoExchanges()
        self.assertIsNone(crypto_exchange.crypto_exchange_name)
        self.assertIsNone(crypto_exchange.fetcher)

    def test_binance_view_init(self):
        binance_view = BinanceView()
        self.assertEqual(binance_view.crypto_exchange_name, 'Binance')
        self.assertEqual(binance_view.fetcher, BinanceFetcher)

    def test_gateio_view_init(self):
        gateio_view = GateioView()
        self.assertEqual(gateio_view.crypto_exchange_name, 'GateIo')
        self.assertEqual(gateio_view.fetcher, GateioFetcher)

    def test_init_coinlist(self):
        coin_list_view = CoinListView()
        self.assertEqual(coin_list_view.crypto_exchange_name, 'CoinList')
        self.assertEqual(coin_list_view.fetcher, CoinListFetcher)

    def test_init_coinbase(self):
        coinbase_view = CoinBaseView()
        self.assertEqual(coinbase_view.crypto_exchange_name, 'CoinBase')
        self.assertEqual(coinbase_view.fetcher, CoinBaseFetcher)

    def test_init_kraken(self):
        kraken_view = KrakenView()
        self.assertEqual(kraken_view.crypto_exchange_name, 'Kraken')
        self.assertEqual(kraken_view.fetcher, KrakenFetcher)

    def test_check_for_errors_from_the_response_to_the_api_call_with_error(self):
        data = {'msg': 'error message'}
        service = 'test_service'
        fetcher = BinanceFetcher
        view = GenericCryptoExchanges(fetcher=fetcher)
        response = view.check_for_errors_from_the_response_to_the_api_call(data, service)
        expected_response = Response({'error': 'error message'}, status=400)
        self.assertEqual(response.data, expected_response.data)
        self.assertEqual(response.status_code, expected_response.status_code)

    def test_check_for_errors_from_the_response_to_the_api_call_without_error(self):
        data = {'result': 'test_result'}
        service = 'test_service'
        fetcher = BinanceFetcher
        view = GenericCryptoExchanges(fetcher=fetcher)
        response = view.check_for_errors_from_the_response_to_the_api_call(data, service)
        self.assertIsNone(response)
