from urllib.request import Request
from rest_framework.exceptions import ValidationError
from django.test import TestCase
from crypto_exchanges.serializers import TokenSerializer
from accounts.models import User
from crypto_exchanges.models import Token, CryptoExchangeAccount
from rest_framework.test import APIRequestFactory


class TokenSerializerTestCase(TestCase):
    """Token serializer unit tests"""

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

    def _assert_token_is_invalid(self, serializer):
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_valid_token_input_data(self):
        data = {
            'user': self.user.id,
            'crypto_exchange_object': self.crypto_exchange_account.id,
            'asset': 'BTC',
            'free_amount': 1.0,
            'locked_amount': 0.0
        }
        serializer = TokenSerializer(data=data, context={'request': self.request})
        self.assertTrue(serializer.is_valid())
        token = serializer.save()
        self.assertIsInstance(token, Token)
        self.assertEqual(token.user, self.user)
        self.assertEqual(token.asset, 'BTC')
        self.assertEqual(token.free_amount, 1.0)
        self.assertEqual(token.locked_amount, 0.0)

    def test_token_creation_with_incorrect_asset_format(self):
        data = {
            'asset': True,
            'free': 1.0,
            'locked': 0.0,
        }
        serializer = TokenSerializer(data=data, context={'request': self.request})
        self._assert_token_is_invalid(serializer)

    def test_token_creation_with_incorrect_free_format(self):
        data = {
            'asset': 'BTC',
            'free': 'not a number',
            'locked': 0.0,
        }
        serializer = TokenSerializer(data=data, context={'request': self.request})
        self._assert_token_is_invalid(serializer)

    def test_token_creation_with_incorrect_locked_format(self):
        data = {
            'asset': 'BTC',
            'free': 1.0,
            'locked': 'not a number',
        }
        serializer = TokenSerializer(data=data, context={'request': self.request})
        self._assert_token_is_invalid(serializer)

    def test_token_creation_with_negative_free_value(self):
        data = {
            'asset': 'BTC',
            'free': -1.0,
            'locked': 1.0,
        }
        serializer = TokenSerializer(data=data, context={'request': self.request})
        self._assert_token_is_invalid(serializer)

    def test_token_creation_with_negative_locked_value(self):
        data = {
            'asset': 'BTC',
            'free': 1.0,
            'locked': -1.0,
        }
        serializer = TokenSerializer(data=data, context={'request': self.request})
        self._assert_token_is_invalid(serializer)

    def test_token_creation_with_missing_asset(self):
        data = {
            'free': 1.0,
            'locked': 1.0,
        }
        serializer = TokenSerializer(data=data, context={'request': self.request})
        self._assert_token_is_invalid(serializer)

    def test_token_creation_with_missing_free_value(self):
        data = {
            'asset': 'BTC',
            'locked': 1.0,
        }
        serializer = TokenSerializer(data=data, context={'request': self.request})
        self._assert_token_is_invalid(serializer)

    def test_token_creation_with_missing_locked_value(self):
        data = {
            'asset': 'BTC',
            'free': 1.0,
        }
        serializer = TokenSerializer(data=data, context={'request': self.request})
        self._assert_token_is_invalid(serializer)
