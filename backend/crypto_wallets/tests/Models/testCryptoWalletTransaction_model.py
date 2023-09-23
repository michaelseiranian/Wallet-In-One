"""Unit tests that will be used to test the CryptoWalletTransaction model."""

from django.test import TestCase
from django.core.exceptions import ValidationError
from accounts.models import User
from crypto_wallets.models import CryptoWallet, CryptoWalletTransaction


class CryptoWalletTestCase(TestCase):
    """Unit tests that will be used to test the CryptoWalletTransaction model."""

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
        self.crypto_wallet_transaction = CryptoWalletTransaction(
            crypto_wallet = self.crypto_wallet,
            value=234.323,
            time=23,

        )

    def _assert_is_valid(self, crypto_wallet_transaction):
        try:
            crypto_wallet_transaction.full_clean()
        except ValidationError:
            self.fail("Crypto wallet transaction is not valid.")

    def _assert_is_invalid(self, crypto_wallet_transaction):
        with self.assertRaises(ValidationError):
            crypto_wallet_transaction.full_clean()

    """Test Set Up"""
    def test_set_up(self):
        self._assert_is_valid(self.crypto_wallet_transaction)

    """Test CryptoWallet"""
    def test_crypto_wallet_must_not_be_blank(self):
        self.crypto_wallet_transaction.crypto_wallet = None
        self._assert_is_invalid(self.crypto_wallet_transaction)

    """Test Value"""
    def test_value_must_not_be_blank(self):
        self.crypto_wallet_transaction.value = None
        self._assert_is_invalid(self.crypto_wallet_transaction)

    def test_value_can_be_integer(self):
        self.crypto_wallet_transaction.value = 234
        self._assert_is_valid(self.crypto_wallet_transaction)

    def test_value_can_be_float(self):
        self.crypto_wallet_transaction.value = 234.2344
        self._assert_is_valid(self.crypto_wallet_transaction)

    """Test Time"""
    def test_time_must_not_be_blank(self):
        self.crypto_wallet_transaction.time = None
        self._assert_is_invalid(self.crypto_wallet_transaction)

    def test_time_is_integer(self):
        self.crypto_wallet_transaction.time = 234
        self._assert_is_valid(self.crypto_wallet_transaction)