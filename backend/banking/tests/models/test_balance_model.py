from django.core.exceptions import ValidationError
from django.test import TestCase
from accounts.models import User
from banking.models import Balance
from djmoney.money import Money
from moneyed.classes import CurrencyDoesNotExist

class BalanceModelTestCase(TestCase):
    """Unit tests for the Balance model."""

    fixtures = [
        'accounts/fixtures/user.json',
        'banking/tests/fixtures/bank_data.json'
    ]

    def setUp(self):
        self.user = User.objects.get(id=1) 
        self.balance = Balance.objects.get(id=1)

    def test_balance_valid(self):
        self._assert_is_valid()

    def test_account_cannot_be_none(self):
        self.balance.account = None
        self._assert_is_invalid()

    def test_date_cannot_be_none(self):
        self.balance.date = None
        self._assert_is_invalid()

    def test_date_cannot_be_invalid_string(self):
        self.balance.date = '110'
        self._assert_is_invalid()

    def test_amount_cannot_be_none(self):
        self.balance.amount = None
        self._assert_is_invalid()

    def test_amount_cannot_be_none(self):
        self.balance.amount = None
        self._assert_is_invalid()

    def test_amount_cannot_be_larger_than_11_digits(self):
        self.balance.amount = Money(1000000000000000000.00,'GBP')
        self._assert_is_invalid()

    def test_amount_can_have_11_digits(self):
        self.balance.amount = Money(100000000.00,'GBP')
        self._assert_is_valid()

    def test_amount_can_have_invalid_currency(self):
        with self.assertRaises(CurrencyDoesNotExist):
            self.balance.amount = Money(1000,'Monopoly Money')
        self._assert_is_valid()

    def test_search_method(self):
        self.assertTrue(Balance.search(self.balance.account, "GBP","2022-11-01").exists())
        
    def test_search_method_when_no_balances(self):
        Balance.objects.all().delete()
        self.assertFalse(Balance.search(self.balance.account, "GBP","2022-11-01").exists())
        
    def _assert_is_valid(self):
        try:
            self.balance.full_clean()
        except (ValidationError):
            self.fail('Test balance should be valid')

    def _assert_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.balance.full_clean()