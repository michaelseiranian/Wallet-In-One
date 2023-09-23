"""Collection of tests that will be used to test the ListCryptoWallet view."""

from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ValidationError
from rest_framework.test import APIClient
from rest_framework import status

from crypto_wallets.views import CryptoWalletViewSet
from accounts.models import User
from crypto_wallets.models import CryptoWallet
from crypto_wallets.serializers import CryptoWalletSerializer


class ListCryptoWalletTestCase(TestCase):
    """Unit tests that will be used to test the ListCryptoWallet view."""

    fixtures = [
        'accounts/fixtures/user.json',
    ]

    def setUp(self):
        super(TestCase, self).setUp()
        self.client = APIClient()
        #self.url = reverse('crypto_wallets')
        self.user = User.objects.get(id=1)
        self.crypto_wallet1 = CryptoWallet(
            user=self.user,
            cryptocurrency="Bitcoin",
            symbol="BTC",
            address="0x0",
            balance=100.00
        )
        self.transaction = {
            'id': 232,
            'value': 434,
            'time': 45,
        }
        self.serializer = {
            'user': User.objects.get(username='@pickles'),
            'id':1,
            'cryptocurrency': 'Bitcoin',
            'symbol': 'BTC',
            'address': '0x0',
            'balance': 100.00,
            'transactions': [self.transaction],
        }

    def test_crypto_wallet_url(self):
        self.url = reverse('crypto_wallet_view_set-list')
        self.assertEqual(self.url, '/crypto_wallets/')

    """Test Get"""
    def test_get(self):
        crypto_wallets = CryptoWallet.objects.filter(user=self.user)
        serializer = CryptoWalletSerializer(crypto_wallets)
        # self.url = reverse('crypto_wallets',kwargs={'account_id':'abc'})
        # response = ListCryptoWallets.get(self, request)
        # self.assertEqual(response, serializer)


    """Test Post"""


    """Test Delete"""
