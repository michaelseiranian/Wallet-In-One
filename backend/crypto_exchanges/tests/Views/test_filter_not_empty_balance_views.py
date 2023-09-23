from django.test import TestCase
from ...views import GenericCryptoExchanges, BinanceView, GateioView, CoinListView, CoinBaseView, KrakenView


class FilterNotEmptyBalanceTestCase(TestCase):

    def test_filter_not_empty_balance(self):
        crypto_exchange = GenericCryptoExchanges()
        with self.assertRaises(TypeError):
            crypto_exchange.filter_not_empty_balance()

    def test_filter_not_empty_balance_binance(self):
        binance_view = BinanceView()
        coin_to_check = {'free': 100}
        self.assertTrue(binance_view.filter_not_empty_balance(coin_to_check))
        coin_to_check = {'free': 0}
        self.assertFalse(binance_view.filter_not_empty_balance(coin_to_check))

    def test_filter_not_empty_balance_gateio(self):
        gateio_view = GateioView()
        coin_to_check = {'available': 100}
        self.assertTrue(gateio_view.filter_not_empty_balance(coin_to_check))
        coin_to_check = {'available': 0}
        self.assertFalse(gateio_view.filter_not_empty_balance(coin_to_check))

    def test_filter_not_empty_balance_coinlist(self):
        coinlist_view = CoinListView()
        coin_to_check = {0: 'BTC', 1: 100}
        self.assertTrue(coinlist_view.filter_not_empty_balance(coin_to_check))
        coin_to_check = {0: 'BTC', 1: 0}
        self.assertFalse(coinlist_view.filter_not_empty_balance(coin_to_check))

    def test_filter_not_empty_balance_coinbase(self):
        coinbase_view = CoinBaseView()
        coin_to_check = {'amount': 100}
        self.assertTrue(coinbase_view.filter_not_empty_balance(coin_to_check))
        coin_to_check = {'amount': 0}
        self.assertFalse(coinbase_view.filter_not_empty_balance(coin_to_check))

    def test_filter_not_empty_balance_kraken(self):
        kraken_view = KrakenView()
        coin_to_check = {0: 'BTC', 1: 100}
        self.assertTrue(kraken_view.filter_not_empty_balance(coin_to_check))
        coin_to_check = {0: 'BTC', 1: 0}
        self.assertFalse(kraken_view.filter_not_empty_balance(coin_to_check))
