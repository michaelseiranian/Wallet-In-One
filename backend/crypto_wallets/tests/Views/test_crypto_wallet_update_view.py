from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from accounts.models import User
from crypto_wallets.models import CryptoWallet


class CryptoWalletUpdateTestCase(TestCase):

    fixtures = [
        'accounts/fixtures/user.json',
    ]

    def setUp(self):
        super(TestCase, self).setUp()
        self.client = APIClient()
        self.user = User.objects.get(id=1)
        self.client.force_authenticate(self.user)
        self.url = reverse('crypto_wallet_update')

        self.crypto_wallet = CryptoWallet(
            pk=1,
            user=self.user,
            cryptocurrency="Bitcoin",
            symbol="BTC",
            address="bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh",
            balance=-1,
            received=-1,
            spent=-1,
            output_count=-1,
            unspent_output_count=-1,
        )
        self.crypto_wallet.save()

    def test_url(self):
        self.assertEqual(self.url, '/crypto_wallets/update')

    def test_put_update(self):
        response = self.client.put(self.url)
        updated_wallet = CryptoWallet.objects.get(address=self.crypto_wallet.address)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(self.crypto_wallet.balance, updated_wallet.balance)
        self.assertNotEqual(self.crypto_wallet.received, updated_wallet.received)
        self.assertNotEqual(self.crypto_wallet.spent, updated_wallet.spent)
        self.assertNotEqual(self.crypto_wallet.output_count, updated_wallet.output_count)
        self.assertNotEqual(self.crypto_wallet.unspent_output_count, updated_wallet.unspent_output_count)

    def test_put_invalid_update(self):
        crypto_wallet = CryptoWallet(
            pk=1,
            user=self.user,
            cryptocurrency="Bitcoin",
            symbol="BTC",
            address="invalid",
            balance=-1,
            received=-1,
            spent=-1,
            output_count=-1,
            unspent_output_count=-1,
        )
        crypto_wallet.save()

        response = self.client.put(self.url)
        updated_wallet = CryptoWallet.objects.filter(address=crypto_wallet.address)
        self.assertFalse(updated_wallet.exists())
