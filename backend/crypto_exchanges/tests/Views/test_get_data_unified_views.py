from django.test import TestCase
from ...views import BinanceView, GateioView, CoinListView, CoinBaseView, KrakenView


class GetDataUnifiedTestCase(TestCase):

    def test_get_data_unified_binance(self):
        binance_view = BinanceView()
        data = {'balances': [{'asset': 'BTC', 'free': 1.0, 'locked': 0.0}]}
        expected = [{'asset': 'BTC', 'free': 1.0, 'locked': 0.0}]
        self.assertEqual(list(binance_view.get_data_unified(data)), expected)

    def test_get_data_unified_gateio(self):
        gateio_view = GateioView()
        data = {'BTC': {'available': 1.0, 'locked': 0.0}}
        self.assertEqual(gateio_view.get_data_unified(data), data)

    def test_get_data_unified_coinlist(self):
        coinlist_view = CoinListView()
        data = {'asset_balances': {'BTC': 1.0, 'ETH': 0.5}}
        expected = [('BTC', 1.0), ('ETH', 0.5)]
        self.assertEqual(list(coinlist_view.get_data_unified(data)), expected)

    def test_get_data_unified_coinbase(self):
        coinbase_view = CoinBaseView()
        data = {'amount': 1.0, 'currency': 'BTC'}
        self.assertEqual(coinbase_view.get_data_unified(data), data)

    def test_get_data_unified_kraken(self):
        kraken_view = KrakenView()
        data = {'result': {'XBT': '1.0', 'ETH': '0.5'}}
        expected = [('XBT', '1.0'), ('ETH', '0.5')]
        self.assertEqual(list(kraken_view.get_data_unified(data)), expected)
