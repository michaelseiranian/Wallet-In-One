from django.test import TestCase
from django.core.exceptions import ValidationError
from accounts.models import User
from crypto_wallets.models import CryptoWallet


class CryptoWalletTestCase(TestCase):

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

    def _assert_is_valid(self, crypto_wallet):
        try:
            crypto_wallet.full_clean()
        except ValidationError:
            self.fail("Crypto wallet is not valid.")

    def _assert_is_invalid(self, crypto_wallet):
        with self.assertRaises(ValidationError):
            crypto_wallet.full_clean()

    """Test Set Up"""
    def test_set_up(self):
        self._assert_is_valid(self.crypto_wallet)

    """Test User"""
    def test_user_must_not_be_blank(self):
        self.crypto_wallet.user = None
        self._assert_is_invalid(self.crypto_wallet)

    """Test Cryptocurrency"""
    def test_cryptocurrency_can_be_less_than_256_characters(self):
        self.crypto_wallet.cryptocurrency = 'a' * 100
        self._assert_is_valid(self.crypto_wallet)

    def test_cryptocurrency_can_equal_256_characters(self):
        self.crypto_wallet.cryptocurrency = 'a' * 256
        self._assert_is_valid(self.crypto_wallet)

    def test_cryptocurrency_cannot_exceed_256_characters(self):
        self.crypto_wallet.cryptocurrency = 'a' * 257
        self._assert_is_invalid(self.crypto_wallet)

    """Test Symbol"""
    def test_symbol_can_be_less_than_16_characters(self):
        self.crypto_wallet.cryptocurrency = 'a' * 10
        self._assert_is_valid(self.crypto_wallet)

    def test_symbol_can_equal_16_characters(self):
        self.crypto_wallet.symbol = 'a' * 16
        self._assert_is_valid(self.crypto_wallet)

    def test_symbol_cannot_exceed_16_characters(self):
        self.crypto_wallet.symbol = 'a' * 17
        self._assert_is_invalid(self.crypto_wallet)

    """Test Address"""
    def test_address_can_be_less_than_256_characters(self):
        self.crypto_wallet.address = 'a' * 200
        self._assert_is_valid(self.crypto_wallet)

    def test_address_can_equal_256_characters(self):
        self.crypto_wallet.address = 'a' * 256
        self._assert_is_valid(self.crypto_wallet)

    def test_address_cannot_exceed_256_characters(self):
        self.crypto_wallet.address = 'a' * 257
        self._assert_is_invalid(self.crypto_wallet)

    def test_address_cannot_be_blank(self):
        self.crypto_wallet.address = ''
        self._assert_is_invalid(self.crypto_wallet)

    """Test Balance"""
    def test_balance_must_not_be_blank(self):
        self.crypto_wallet.balance = None
        self._assert_is_invalid(self.crypto_wallet)

    def test_balance_can_be_integer(self):
        self.crypto_wallet.balance = 234
        self._assert_is_valid(self.crypto_wallet)

    def test_balance_can_be_float(self):
        self.crypto_wallet.balance = 234.2344
        self._assert_is_valid(self.crypto_wallet)

    """Test Received"""

    def test_received_must_not_be_blank(self):
        self.crypto_wallet.received = None
        self._assert_is_invalid(self.crypto_wallet)

    def test_received_can_be_integer(self):
        self.crypto_wallet.received = 234
        self._assert_is_valid(self.crypto_wallet)

    def test_received_can_be_float(self):
        self.crypto_wallet.received = 234.2344
        self._assert_is_valid(self.crypto_wallet)

    """Test Spent"""

    def test_spent_must_not_be_blank(self):
        self.crypto_wallet.spent = None
        self._assert_is_invalid(self.crypto_wallet)

    def test_spent_can_be_integer(self):
        self.crypto_wallet.spent = 234
        self._assert_is_valid(self.crypto_wallet)

    def test_spent_can_be_float(self):
        self.crypto_wallet.spent = 234.2344
        self._assert_is_valid(self.crypto_wallet)

    """Test Output Count"""

    def test_output_count_must_not_be_blank(self):
        self.crypto_wallet.output_count = None
        self._assert_is_invalid(self.crypto_wallet)

    def test_output_count_is_integer(self):
        self.crypto_wallet.output_count = 234
        self._assert_is_valid(self.crypto_wallet)

    """Test Unspent Output Count"""

    def test_unspent_output_count_must_not_be_blank(self):
        self.crypto_wallet.unspent_output_count = None
        self._assert_is_invalid(self.crypto_wallet)

    def test_unspent_output_count_is_integer(self):
        self.crypto_wallet.unspent_output_count = 234
        self._assert_is_valid(self.crypto_wallet)
