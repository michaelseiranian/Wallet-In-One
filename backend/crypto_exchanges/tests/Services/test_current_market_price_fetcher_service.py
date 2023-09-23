from django.test import TestCase
from unittest.mock import patch
from crypto_exchanges.services import *
from accounts.models import *


class TestCurrentMarketPriceFetcher(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user('testuser', 'test@example.com', 'password')

    def setUp(self):
        self.fetcher = CurrentMarketPriceFetcher(self.user)
        self.market_fetcher = CurrentMarketPriceFetcher(self.user)

        self.exchange = CryptoExchangeAccount.objects.create(
            user=self.user,
            crypto_exchange_name='Test Exchange',
            api_key='api_key',
            secret_key='secret_key'
        )

        self.token1 = Token.objects.create(
            user=self.user,
            crypto_exchange_object=self.exchange,
            asset='BTC',
            free_amount=1.0,
            locked_amount=0.0
        )
        self.token2 = Token.objects.create(
            user=self.user,
            crypto_exchange_object=self.exchange,
            asset='ETH',
            free_amount=2.0,
            locked_amount=0.5
        )

    @patch('requests.get')
    def test_get_crypto_price(self, mock_get):
        mock_get.return_value.json.return_value = {'GBP': 123.45}
        price = self.fetcher.get_crypto_price('BTC')
        self.assertEqual(price, float('123.45'))

        mock_get.return_value.json.return_value = {}
        price = self.fetcher.get_crypto_price('BTC')
        self.assertEqual(price, float('0.0'))

    @patch('crypto_exchanges.services.CurrentMarketPriceFetcher.get_crypto_price')
    def test_total_user_balance_crypto(self, mock_get_crypto_price):
        mock_get_crypto_price.side_effect = lambda asset: 10000.0 if asset == 'BTC' else 200.0

        expected_balance = (10000.0 * (1.0 + 0.0)) + (200.0 * (2.0 + 0.5))

        actual_balance = self.market_fetcher.total_user_balance_crypto()

        self.assertAlmostEqual(actual_balance, expected_balance, places=2)

    @patch('crypto_exchanges.services.CurrentMarketPriceFetcher.get_crypto_price')
    def test_chart_breakdown_crypto_free(self, mock_get_crypto_price):
        mock_get_crypto_price.side_effect = lambda asset: 10000.0 if asset == 'BTC' else 200.0

        breakdown = self.market_fetcher.chart_breakdown_crypto_free()

        expected_breakdown = [{'x': 'BTC', 'y': 10000.0}, {'x': 'ETH', 'y': 400.0}]
        self.assertEqual(breakdown, expected_breakdown)

    @patch('crypto_exchanges.services.CurrentMarketPriceFetcher.get_crypto_price')
    def test_chart_breakdown_crypto_locked(self, mock_get_crypto_price):
        mock_get_crypto_price.side_effect = lambda asset: 10000.0 if asset == 'BTC' else 200.0

        breakdown = self.market_fetcher.chart_breakdown_crypto_locked()

        expected_breakdown = [{'x': 'BTC', 'y': 0.0}, {'x': 'ETH', 'y': 100.0}]
        self.assertEqual(breakdown, expected_breakdown)

    @patch('crypto_exchanges.services.CurrentMarketPriceFetcher.get_crypto_price')
    def test_get_exchange_balance(self, mock_get_crypto_price):
        mock_get_crypto_price.side_effect = lambda asset: 10000.0 if asset == 'BTC' else 200.0

        actual_balance = self.market_fetcher.get_exchange_balance(self.exchange)

        expected_balance = (10000.0 * (1.0 + 0.0)) + (200.0 * (2.0 + 0.5))
        self.assertAlmostEqual(actual_balance, expected_balance, places=2)

    @patch('crypto_exchanges.services.CurrentMarketPriceFetcher.get_crypto_price')
    def test_get_exchange_token_breakdown(self, mock_get_crypto_price):
        mock_get_crypto_price.side_effect = lambda asset: 10000.0 if asset == 'BTC' else 200.0

        breakdown = self.market_fetcher.get_exchange_token_breakdown(self.exchange)

        expected_breakdown = {
            "balance": 10500.0,
            "token_data": [
                {"x": "ETH: £500.0", "y": 500.0},
                {"x": "BTC: £10000.0", "y": 10000.0}
            ]
        }
        self.assertEqual(breakdown, expected_breakdown)

    @patch('crypto_exchanges.services.CurrentMarketPriceFetcher.get_crypto_price')
    def test_chart_breakdown_crypto_exchanges(self, mock_get_crypto_price):
        mock_get_crypto_price.side_effect = lambda asset: 10000.0 if asset == 'BTC' else 200.0

        breakdown = self.market_fetcher.chart_breakdown_crypto_exchanges()

        expected_breakdown = [
            {'x': 'Test Exchange', 'y': 10500.0, 'id': self.exchange.id},
        ]
        self.assertEqual(breakdown, expected_breakdown)
