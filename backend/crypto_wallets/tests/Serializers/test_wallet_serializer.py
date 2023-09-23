from django.test import TestCase
from rest_framework import serializers

from crypto_wallets.models import CryptoWallet
from crypto_wallets.serializers import CryptoWalletSerializer
from accounts.models import User
from rest_framework.test import APIRequestFactory


class WalletSerializerTestCase(TestCase):

    fixtures = [
        'accounts/fixtures/user.json',
    ]

    def setUp(self):
        self.user = User.objects.get(id=1)
        self.transaction = {
            'value': 434,
            'time': 450000,
        }
        self.serializer_input = {
            'cryptocurrency': 'Bitcoin',
            'symbol': 'BTC',
            'address': '0x0',
            'balance': 234,
            'received': 12.0,
            'spent': 10.0,
            'output_count': 100,
            'unspent_output_count': 50,
            'transactions': [self.transaction],
        }
        request = APIRequestFactory().post('/')
        request.user = self.user
        self.context = {'request': request}

    def test_valid_data_wallet_serializer(self):
        serializer = CryptoWalletSerializer(data=self.serializer_input, context=self.context)
        self.assertTrue(serializer.is_valid())

    def test_serializer_uses_model_validation(self):
        self.serializer_input['balance'] = 'badbalance'
        serializer = CryptoWalletSerializer(data=self.serializer_input, context=self.context)
        self.assertFalse(serializer.is_valid())

    def test_necessary_fields_in_wallet_serializer(self):
        serializer = CryptoWalletSerializer()
        self.assertIn('id', serializer.fields)
        self.assertIn('user', serializer.fields)
        self.assertIn('cryptocurrency', serializer.fields)
        self.assertIn('symbol', serializer.fields)
        self.assertIn('address', serializer.fields)
        self.assertIn('balance', serializer.fields)
        self.assertIn('received', serializer.fields)
        self.assertIn('spent', serializer.fields)
        self.assertIn('output_count', serializer.fields)
        self.assertIn('unspent_output_count', serializer.fields)
        self.assertIn('transactions', serializer.fields)

    def test_serializer_fields_are_not_required(self):
        serializer_input = {
            'cryptocurrency': 'Bitcoin',
            'symbol': 'BTC',
            'address': '0x0',
        }
        serializer = CryptoWalletSerializer(data=serializer_input, context=self.context)
        serializer.is_valid()

    def test_serializer_is_valid(self):
        serializer = CryptoWalletSerializer(data=self.serializer_input, context=self.context)
        serializer.is_valid()
        self.assertEqual(serializer.validated_data['cryptocurrency'], self.serializer_input['cryptocurrency'])
        self.assertEqual(serializer.validated_data['symbol'], self.serializer_input['symbol'])
        self.assertEqual(serializer.validated_data['address'], self.serializer_input['address'])
        self.assertEqual(serializer.validated_data['balance'], self.serializer_input['balance'])
        self.assertEqual(serializer.validated_data['received'], self.serializer_input['received'])
        self.assertEqual(serializer.validated_data['spent'], self.serializer_input['spent'])
        self.assertEqual(serializer.validated_data['output_count'], self.serializer_input['output_count'])
        self.assertEqual(serializer.validated_data['unspent_output_count'], self.serializer_input['unspent_output_count'])
        self.assertEqual(serializer.validated_data['cryptowallettransaction_set'], self.serializer_input['transactions'])

    def test_serializer_does_not_return_transactions_when_context_passed(self):
        self.context['exclude_transactions'] = True
        serializer = CryptoWalletSerializer(context=self.context)
        self.assertNotIn('transactions', serializer.fields)

    def test_serializer_create(self):
        serializer_input = {
            'cryptocurrency': 'Bitcoin',
            'symbol': 'BTC',
            'address': '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa',
        }
        wallet_count_before = CryptoWallet.objects.count()
        serializer = CryptoWalletSerializer(data=serializer_input, context=self.context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        wallet_count_after = CryptoWallet.objects.count()
        self.assertEqual(wallet_count_after, wallet_count_before + 1)
        saved_wallet = CryptoWallet.objects.get(address=serializer_input['address'])
        self.assertEqual(saved_wallet.user, self.user)
        self.assertEqual(saved_wallet.cryptocurrency, serializer_input['cryptocurrency'])
        self.assertEqual(saved_wallet.symbol, serializer_input['symbol'])
        self.assertEqual(saved_wallet.address, serializer_input['address'])

    def test_serializer_raises_error_on_unknown_address(self):
        serializer_input = {
            'cryptocurrency': 'Bitcoin',
            'symbol': 'BTC',
            'address': '???',
        }
        serializer = CryptoWalletSerializer(data=serializer_input, context=self.context)
        serializer.is_valid()
        self.assertRaises(serializers.ValidationError, serializer.save)
