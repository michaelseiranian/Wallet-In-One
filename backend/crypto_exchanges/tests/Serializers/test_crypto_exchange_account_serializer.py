from crypto_exchanges.serializers import CryptoExchangeAccountSerializer
from accounts.models import User
from crypto_exchanges.models import CryptoExchangeAccount
from rest_framework.test import APIRequestFactory
from django.test import TestCase
from urllib.request import Request
from rest_framework.exceptions import ValidationError


class CryptoExchangeAccountSerializerTestCase(TestCase):
    """CryptoExchangeAccountSerializer unit tests"""

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username='@user', first_name='Name', last_name='Lastname',
                                             email='namelastname@example.org')
        self.request = Request(self.factory.post('/'))
        self.request.user = self.user

    def _assert_crypto_exchange_account_serializer_is_invalid(self, serializer):
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_valid_crypto_exchange_account_serializer_input_data(self):
        data = {
            'crypto_exchange_name': 'Binance',
            'api_key': 'myApiKey',
            'secret_key': 'mySecretKey',
        }
        serializer = CryptoExchangeAccountSerializer(data=data, context={'request': self.request})
        self.assertTrue(serializer.is_valid())
        account = serializer.save()
        self.assertIsInstance(account, CryptoExchangeAccount)
        self.assertEqual(account.user, self.user)
        self.assertEqual(account.crypto_exchange_name, 'Binance')
        self.assertEqual(account.api_key, 'myApiKey')
        self.assertEqual(account.secret_key, 'mySecretKey')

    def test_crypto_exchange_account_serializer_creation_with_missing_crypto_exchange(self):
        data = {
            'api_key': 'myApiKey',
            'secret_key': 'mySecretKey',
        }
        serializer = CryptoExchangeAccountSerializer(data=data, context={'request': self.request})
        self._assert_crypto_exchange_account_serializer_is_invalid(serializer)

    def test_crypto_exchange_account_serializer_creation_with_missing_api_key(self):
        data = {
            'crypto_exchange': 'Binance',
            'secret_key': 'mySecretKey',
        }
        serializer = CryptoExchangeAccountSerializer(data=data, context={'request': self.request})
        self._assert_crypto_exchange_account_serializer_is_invalid(serializer)

    def test_crypto_exchange_account_serializer_creation_with_missing_secret_key(self):
        data = {
            'crypto_exchange': 'Binance',
            'api_key': 'myApiKey',
        }
        serializer = CryptoExchangeAccountSerializer(data=data, context={'request': self.request})
        self._assert_crypto_exchange_account_serializer_is_invalid(serializer)

    def test_crypto_exchange_account_serializer_creation_with_incorrect_crypto_exchange_format(self):
        data = {
            'crypto_exchange': True,
            'api_key': 'myApiKey',
            'secret_key': 'mySecretKey'
        }
        serializer = CryptoExchangeAccountSerializer(data=data, context={'request': self.request})
        self._assert_crypto_exchange_account_serializer_is_invalid(serializer)

    def test_crypto_exchange_account_serializer_creation_with_incorrect_api_key_format(self):
        data = {
            'crypto_exchange': 'Binance',
            'api_key': True,
            'secret_key': 'mySecretKey'
        }
        serializer = CryptoExchangeAccountSerializer(data=data, context={'request': self.request})
        self._assert_crypto_exchange_account_serializer_is_invalid(serializer)

    def test_crypto_exchange_account_serializer_creation_with_incorrect_secret_key_format(self):
        data = {
            'crypto_exchange': 'Binance',
            'api_key': 'myApiKey',
            'secret_key': True
        }
        serializer = CryptoExchangeAccountSerializer(data=data, context={'request': self.request})
        self._assert_crypto_exchange_account_serializer_is_invalid(serializer)