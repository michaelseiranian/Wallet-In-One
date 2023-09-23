from django.test import TestCase
from django.core.exceptions import ValidationError
from accounts.models import User
from crypto_exchanges.models import CryptoExchangeAccount, Transaction


class TransactionModelTestCase(TestCase):
    """Unit tests for the transaction model"""

    fixtures = ['accounts/fixtures/user.json']

    def setUp(self):
        super(TestCase, self).setUp()

        self.user = User.objects.get(id=1)

        self.crypto_exchange_account = CryptoExchangeAccount(
            user=self.user,
            crypto_exchange_name='Kraken',
            api_key='owibhouibh034985',
            secret_key='oefigno23487h',
        )

        self.crypto_exchange_account.save()

        self.transaction = Transaction(crypto_exchange_object=self.crypto_exchange_account,
                           asset="ETH",
                           transaction_type="buy",
                           amount="0.2134")

    def _assert_transaction_is_valid(self, transaction):
        try:
            transaction.full_clean()
        except ValidationError:
            self.fail("Invalid transaction")

    def _assert_transaction_is_invalid(self, transaction):
        with self.assertRaises(ValidationError):
            transaction.full_clean()

    def test_asset_not_blank(self):
        self.transaction.asset = None
        self._assert_transaction_is_invalid(self.transaction)

    def test_asset_can_be_15_chars(self):
        self.transaction.asset = 'Q' * 15
        self._assert_transaction_is_valid(self.transaction)

    def test_asset_cannot_exceed_15_chars(self):
        self.transaction.asset = 'Q' * 16
        self._assert_transaction_is_invalid(self.transaction)

    def test_transaction_type_can_be_20_chars(self):
        self.transaction.transaction_type = 'Q' * 20
        self._assert_transaction_is_valid(self.transaction)

    def test_transaction_type_cannot_exceed_20_chars(self):
        self.transaction.transaction_type = 'Q' * 21
        self._assert_transaction_is_invalid(self.transaction)

    def test_amount_cannot_be_negative(self):
        self.transaction.amount = -1.0
        self._assert_transaction_is_invalid(self.transaction)
