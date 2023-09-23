from django.core.exceptions import ValidationError
from django.test import TestCase
from accounts.models import User
from banking.models import Transaction
from djmoney.money import Money
from moneyed.classes import CurrencyDoesNotExist

class TransactionModelTestCase(TestCase):
    """Unit tests for the Transaction model."""

    fixtures = [
        'accounts/fixtures/user.json',
        'banking/tests/fixtures/bank_data.json'
    ]

    def setUp(self):
        self.user = User.objects.get(id=1) 
        self.transaction = Transaction.objects.get(id=1)
        self.transaction2 = Transaction.objects.get(id=2)

    def test_transaction_valid(self):
        self._assert_is_valid()

    def test_account_cannot_be_none(self):
        self.transaction.account = None
        self._assert_is_invalid()

    def test_id_cannot_be_none(self):
        self.transaction.id = None
        self._assert_is_invalid()

    def test_id_cannot_be_larger_than_1024(self):
        self.transaction.id = '1'*1025
        self._assert_is_invalid()

    def test_id_can_be_1024(self):
        self.transaction.id = '1'*1024
        self._assert_is_valid()

    def test_info_cannot_be_larger_than_4096(self):
        self.transaction.info = '1'*4097
        self._assert_is_invalid()

    def test_info_can_be_4096(self):
        self.transaction.info = '1'*4096
        self._assert_is_valid()

    def test_time_cannot_be_none(self):
        self.transaction.time = None
        self._assert_is_invalid()

    def test_time_cannot_be_invalid_string(self):
        self.transaction.time = '110'
        self._assert_is_invalid()

    def test_amount_cannot_be_none(self):
        self.transaction.amount = None
        self._assert_is_invalid()

    def test_amount_cannot_be_none(self):
        self.transaction.amount = None
        self._assert_is_invalid()

    def test_amount_cannot_be_larger_than_11_digits(self):
        self.transaction.amount = Money(1000000000000000000.00,'GBP')
        self._assert_is_invalid()

    def test_amount_can_have_11_digits(self):
        self.transaction.amount = Money(100000000.00,'GBP')
        self._assert_is_valid()

    def test_amount_can_have_invalid_currency(self):
        with self.assertRaises(CurrencyDoesNotExist):
            self.transaction.amount = Money(1000,'Monopoly Money')
        self._assert_is_valid()

    def _assert_is_valid(self):
        try:
            self.transaction.full_clean()
        except (ValidationError):
            self.fail('Test Transaction should be valid')

    def _assert_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.transaction.full_clean()