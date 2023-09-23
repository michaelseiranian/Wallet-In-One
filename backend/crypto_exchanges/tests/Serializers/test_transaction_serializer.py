from urllib.request import Request
from rest_framework.exceptions import ValidationError
from django.test import TestCase
from crypto_exchanges.serializers import TransactionSerializer
from accounts.models import User
from crypto_exchanges.models import CryptoExchangeAccount, Transaction
from rest_framework.test import APIRequestFactory
from datetime import datetime
import zoneinfo


class TransactionSerializerTestCase(TestCase):
    """TransactionSerializer unit tests"""

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username='@user', first_name='Name', last_name='Lastname',
                                             email='namelastname@example.org')
        self.request = Request(self.factory.post('/'))
        self.request.user = self.user
        self.crypto_exchange_account = CryptoExchangeAccount.objects.create(
            user=self.user,
            crypto_exchange_name='Binance',
            api_key='wfeioguhwe549876y43jh',
            secret_key='wfjbh234987trfhu'
        )

    def _assert_transaction_is_invalid(self, serializer):
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_valid_transaction_input_data(self):
        data = {
            'crypto_exchange_object': self.crypto_exchange_account.id,
            'asset': 'BTCUSDT',
            'transaction_type': 'buy',
            'amount': 40.0,
            'timestamp': datetime(2023, 4, 15, 18, 0, 0)
        }
        serializer = TransactionSerializer(data=data, context={'request': self.request})
        self.assertTrue(serializer.is_valid())
        transaction = serializer.save()
        self.assertIsInstance(transaction, Transaction)
        self.assertEqual(transaction.crypto_exchange_object, self.crypto_exchange_account)
        self.assertEqual(transaction.asset, 'BTCUSDT')
        self.assertEqual(transaction.transaction_type, "buy")
        self.assertEqual(transaction.amount, 40)
        self.assertEqual(transaction.timestamp, datetime(2023, 4, 15, 18, 0, tzinfo=zoneinfo.ZoneInfo(key='UTC')))
