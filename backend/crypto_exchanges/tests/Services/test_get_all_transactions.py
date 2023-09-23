from django.test import TestCase, RequestFactory
from accounts.models import User
from crypto_exchanges.models import *
from crypto_exchanges.services import *


class TestGetAllTransactions(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', first_name='Lesya', last_name='Abakhova',
                                             email='example@hse.edu.ru', password='testpassword')
        self.crypto_exchange = CryptoExchangeAccount.objects.create(user=self.user, crypto_exchange_name='Binance')
        self.transaction_1 = Transaction.objects.create(crypto_exchange_object=self.crypto_exchange, asset='BTCUSDT',
                                                        amount=1.0, transaction_type='BUY',
                                                        timestamp='2022-03-20T12:00:00Z')
        self.transaction_2 = Transaction.objects.create(crypto_exchange_object=self.crypto_exchange, asset='ETHUSDT',
                                                        transaction_type='SELL', amount=2.0,
                                                        timestamp='2022-03-21T12:00:00Z')

    def test_get_all_transactions(self):
        url = '/transactions/'
        request = self.factory.get(url)
        request.user = self.user
        response = get_all_transactions(request)
        expected_data = TransactionSerializer([self.transaction_1, self.transaction_2], many=True).data
        self.assertEqual(response, expected_data)

    def test_empty_transactions(self):
        request = RequestFactory().get('/')
        request.user = self.user
        self.transaction_1.delete()
        self.transaction_2.delete()
        transactions = Transaction.objects.filter(crypto_exchange_object__user=self.user)
        self.assertEqual(transactions.count(), 0)

        response = get_all_transactions(request)
        self.assertEqual(response, ['empty'])
