from django.test import TestCase
from crypto_wallets.serializers import CryptoWalletSerializer
from accounts.models import User
from crypto_wallets.models import CryptoWallet
from django.urls import reverse
from rest_framework.test import APIRequestFactory


class WalletSerializerTestCase(TestCase):
    """Unit tests for WalletSerializer class."""

    fixtures = [
        'accounts/fixtures/user.json',
    ]

    def setUp(self):
        self.user = User.objects.get(id=1)
        self.transaction = {
            'id': 232,
            'value': 434,
            'time': 45,
        }
        self.serializer_input = {
            'user': User.objects.get(id=1),
            'id':1,
            'cryptocurrency': 'Bitcoin',
            'symbol': 'BTC',
            'address': '0x0',
            'balance': 234,
            'transactions': [self.transaction],
        }

    def test_valid_data_wallet_serializer(self):
        request = APIRequestFactory().post('/')
        request.user = self.user
        serializer = CryptoWalletSerializer(data=self.serializer_input, context={'request': request})
        self.assertTrue(serializer.is_valid())

    def test_necessary_fields_in_wallet_serializer(self):
        serializer = CryptoWalletSerializer()
        self.assertIn('user', serializer.fields)
        self.assertIn('id', serializer.fields)
        self.assertIn('cryptocurrency', serializer.fields)
        self.assertIn('symbol', serializer.fields)
        self.assertIn('address', serializer.fields)
        self.assertIn('balance', serializer.fields)
        self.assertIn('transactions', serializer.fields)

    def test_form_uses_model_validation(self):
        self.serializer_input['balance'] = 'badbalance'
        request = APIRequestFactory().post('/')
        request.user = self.user
        serializer = CryptoWalletSerializer(data=self.serializer_input, context={'request': request})
        self.assertFalse(serializer.is_valid())