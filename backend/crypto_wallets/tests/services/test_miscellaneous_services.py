from django.test import TestCase

from accounts.models import User
from crypto_wallets.models import CryptoWallet
from crypto_wallets.services import get_crypto_price, total_user_balance_crypto, chart_breakdown_crypto


class CryptoWalletMiscellaneousTestCase(TestCase):

    fixtures = [
        'accounts/fixtures/user.json',
    ]

    def setUp(self):
        super(TestCase, self).setUp()
        self.user = User.objects.get(id=1)
        self.crypto_wallet = CryptoWallet(
            user=self.user,
            cryptocurrency="Bitcoin",
            symbol="BTC",
            address="0x0",
            balance=100.00,
            received=300.00,
            spent=200.00,
            output_count=50,
            unspent_output_count=20
        )
        self.crypto_wallet.save()

    def test_get_crypto_price(self):
        crypto_price = get_crypto_price('BTC')
        self.assertIsInstance(crypto_price, float)

    def test_invalid_get_crypto_price(self):
        crypto_price = get_crypto_price('UNKNOWN')
        self.assertEqual(crypto_price, 0)

    def test_total_user_balance_crypto(self):
        crypto_wallet_two = CryptoWallet(
            user=self.user,
            cryptocurrency="Bitcoin",
            symbol="BTC",
            address="0x1",
            balance=100.00,
            received=300.00,
            spent=200.00,
            output_count=50,
            unspent_output_count=20
        )
        crypto_wallet_two.save()

        total_user_balance = total_user_balance_crypto(self.user)
        self.assertGreater(total_user_balance, 0)

    def test_total_user_balance_crypto_when_empty(self):
        CryptoWallet.objects.all().delete()
        total_user_balance = total_user_balance_crypto(self.user)
        self.assertEqual(total_user_balance, 0)

    def test_total_user_balance_crypto_with_multiple_users(self):
        other_user = User.objects.get(id=2)
        crypto_wallet_two = CryptoWallet(
            user=other_user,
            cryptocurrency="Bitcoin",
            symbol="BTC",
            address="0x1",
            balance=50.00,
            received=300.00,
            spent=200.00,
            output_count=50,
            unspent_output_count=20
        )
        crypto_wallet_two.save()

        total_user_balance_one = total_user_balance_crypto(self.user)
        total_user_balance_two = total_user_balance_crypto(other_user)
        self.assertNotEqual(total_user_balance_one, total_user_balance_two)

    def test_chart_breakdown_crypto(self):
        crypto_wallet_two = CryptoWallet(
            user=self.user,
            cryptocurrency="Bitcoin",
            symbol="BTC",
            address="0x1",
            balance=100.00,
            received=300.00,
            spent=200.00,
            output_count=50,
            unspent_output_count=20
        )
        crypto_wallet_two.save()

        chart_breakdown = chart_breakdown_crypto(self.user)
        self.assertEqual(len(chart_breakdown), 2)

    def test_chart_breakdown_crypto_when_empty(self):
        CryptoWallet.objects.all().delete()
        chart_breakdown = chart_breakdown_crypto(self.user)
        self.assertIsNone(chart_breakdown)

    def test_chart_breakdown_crypto_with_multiple_users(self):
        other_user = User.objects.get(id=2)
        crypto_wallet_two = CryptoWallet(
            user=other_user,
            cryptocurrency="Bitcoin",
            symbol="BTC",
            address="0x1",
            balance=100.00,
            received=300.00,
            spent=200.00,
            output_count=50,
            unspent_output_count=20
        )
        crypto_wallet_two.save()

        chart_breakdown_one = chart_breakdown_crypto(self.user)
        chart_breakdown_two = chart_breakdown_crypto(self.user)
        self.assertEqual(len(chart_breakdown_one), 1)
        self.assertEqual(len(chart_breakdown_two), 1)
