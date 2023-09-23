from django.test import TestCase
from accounts.models import User
from unittest.mock import patch
from ...models import CryptoExchangeAccount, Transaction
from ...services import CurrentMarketPriceFetcher, get_most_expensive_transaction


class GetMostExpensiveTransactionTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.crypto_exchange_account = CryptoExchangeAccount.objects.create(
            user=self.user,
            crypto_exchange_name='TestExchange',
            api_key='testapikey',
            secret_key='testsecretkey'
        )
        self.transaction1 = Transaction.objects.create(
            crypto_exchange_object=self.crypto_exchange_account,
            asset='BTC',
            transaction_type='buy',
            amount=0.5
        )
        self.transaction2 = Transaction.objects.create(
            crypto_exchange_object=self.crypto_exchange_account,
            asset='ETH',
            transaction_type='sell',
            amount=2.0
        )

    @patch.object(CurrentMarketPriceFetcher, 'get_crypto_price')
    def test_get_most_expensive_transaction(self, mock_get_crypto_price):
        mock_get_crypto_price.side_effect = lambda symbol: {'BTC': 30000.00, 'ETH': 2000.00}[symbol]

        self.client.login(username='testuser', password='testpassword')
        request = self.client.get('/crypto-exchanges/get_insights/').wsgi_request
        request.user = self.user

        result = get_most_expensive_transaction(request)
        self.assertEqual(result, (
        'BTC', 0.5, 15000, 'buy', self.transaction1.timestamp.strftime('%Y-%m-%d %H:%M:%S'), 'TestExchange'))

    @patch.object(CurrentMarketPriceFetcher, 'get_crypto_price')
    def test_get_most_expensive_transaction_with_no_transactions(self, mock_get_crypto_price):
        mock_get_crypto_price.side_effect = lambda symbol: {'BTC': 30000.00, 'ETH': 2000.00}[symbol]
        self.transaction1.delete()
        self.transaction2.delete()
        self.client.login(username='testuser', password='testpassword')
        request = self.client.get('/crypto-exchanges/get_insights/').wsgi_request
        request.user = self.user

        result = get_most_expensive_transaction(request)
        self.assertEqual(result, ('empty', 0.0, 0.0, None, None, None))
