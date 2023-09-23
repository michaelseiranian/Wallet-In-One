"""Tests of the stock account model."""
from django.test import TestCase
from django.core.exceptions import ValidationError
from stocks.models import StockAccount
from djmoney.money import Money
from moneyed.classes import CurrencyDoesNotExist
from django.db import models
from djmoney.models.fields import MoneyField
from accounts.models import User


""" Unit Tests for the Stock Account Model """
class StockAccountModelTestCase(TestCase):

    fixtures = [
        'stocks/tests/fixtures/stocks.json',
        'stocks/tests/fixtures/user.json',
    ]

    def setUp(self):
        self.stockAccount = StockAccount.objects.get(account_id='1')

    def _assert_stock_is_valid(self, stockAccount):
        try:
            stockAccount.full_clean()
        except ValidationError:
            self.fail("Stock Account is not valid.")

    def _assert_stock_is_invalid(self, stockAccount):
        with self.assertRaises(ValidationError):
            stockAccount.full_clean()

    def test_stock_account_is_valid(self):
        self._assert_stock_is_valid(self.stockAccount)

    # Tests for User Foreign Key Field

    def test_user_foreign_key_field(self):
        field = StockAccount._meta.get_field('user')
        self.assertIsInstance(field, models.ForeignKey)
        self.assertEqual(field.many_to_one, True)
        self.assertFalse(field.blank)

    def test_user_on_delete_cascade(self):
        user = User.objects.get(pk=3)
        user.delete()
        self.assertFalse(StockAccount.objects.filter(account_id='1').exists())

    # Tests for Account ID field

    def test_account_id_field(self):
        field = StockAccount._meta.get_field('account_id')
        self.assertIsInstance(field, models.CharField)
        self.assertEqual(field.max_length, 1024)
        self.assertFalse(field.blank)
        self.assertTrue(field.primary_key)
        self.assertTrue(field.editable)

    def test_account_id_cannot_be_blank(self):
        self.stockAccount.account_id = ''
        self._assert_stock_is_invalid(self.stockAccount)

    def test_account_id_cannot_be_none(self):
        self.stockAccount.account_id = None
        self._assert_stock_is_invalid(self.stockAccount)

    def test_account_id_can_be_20_characters_long(self):
        self.stockAccount.account_id = 'a' * 20
        self._assert_stock_is_valid(self.stockAccount)

    def test_account_id_can_be_1024_characters_long(self):
        self.stockAccount.account_id = 'a' * 1024
        self._assert_stock_is_valid(self.stockAccount)

    def test_account_id_cannot_be_1025_characters_long(self):
        self.stockAccount.account_id = 'a' * 1025
        self._assert_stock_is_invalid(self.stockAccount)

    def test_account_id_can_contain_numbers(self):
        self.stockAccount.account_id = '123'
        self._assert_stock_is_valid(self.stockAccount)

    def test_account_id_can_contain_special_characters(self):
        self.stockAccount.account_id = '_@*&'
        self._assert_stock_is_valid(self.stockAccount)

    # Tests for Access Token field

    def test_access_token_field(self):
        field = StockAccount._meta.get_field('access_token')
        self.assertIsInstance(field, models.CharField)
        self.assertEqual(field.max_length, 1024)
        self.assertFalse(field.blank)
        self.assertTrue(field.editable)

    def test_access_token_cannot_be_blank(self):
        self.stockAccount.access_token = ''
        self._assert_stock_is_invalid(self.stockAccount)

    def test_access_token_cannot_be_none(self):
        self.stockAccount.access_token = None
        self._assert_stock_is_invalid(self.stockAccount)

    def test_access_token_can_be_20_characters_long(self):
        self.stockAccount.access_token = 'a' * 20
        self._assert_stock_is_valid(self.stockAccount)

    def test_access_token_can_be_1024_characters_long(self):
        self.stockAccount.access_token = 'a' * 1024
        self._assert_stock_is_valid(self.stockAccount)

    def test_access_token_cannot_be_1025_characters_long(self):
        self.stockAccount.access_token = 'a' * 1025
        self._assert_stock_is_invalid(self.stockAccount)

    def test_access_token_can_contain_numbers(self):
        self.stockAccount.access_token = '123'
        self._assert_stock_is_valid(self.stockAccount)

    def test_access_token_can_contain_special_characters(self):
        self.stockAccount.access_token = '_@*&'
        self._assert_stock_is_valid(self.stockAccount)

    # Tests for Name field

    def test_name_field(self):
        field = StockAccount._meta.get_field('name')
        self.assertIsInstance(field, models.CharField)
        self.assertEqual(field.max_length, 1024)
        self.assertFalse(field.blank)
        self.assertTrue(field.editable)

    def test_name_cannot_be_blank(self):
        self.stockAccount.name = ''
        self._assert_stock_is_invalid(self.stockAccount)

    def test_name_cannot_be_none(self):
        self.stockAccount.name = None
        self._assert_stock_is_invalid(self.stockAccount)

    def test_name_can_be_20_characters_long(self):
        self.stockAccount.name = 'a' * 20
        self._assert_stock_is_valid(self.stockAccount)

    def test_name_can_be_1024_characters_long(self):
        self.stockAccount.name = 'a' * 1024
        self._assert_stock_is_valid(self.stockAccount)

    def test_name_cannot_be_1025_characters_long(self):
        self.stockAccount.name = 'a' * 1025
        self._assert_stock_is_invalid(self.stockAccount)

    def test_name_can_contain_numbers(self):
        self.stockAccount.name = '123'
        self._assert_stock_is_valid(self.stockAccount)

    def test_name_can_contain_special_characters(self):
        self.stockAccount.name = '_@*&'
        self._assert_stock_is_valid(self.stockAccount)

    # Tests for Institution Name field

    def test_institution_name_field(self):
        field = StockAccount._meta.get_field('institution_name')
        self.assertIsInstance(field, models.CharField)
        self.assertEqual(field.max_length, 1024)
        self.assertFalse(field.blank)
        self.assertTrue(field.editable)

    def test_institution_name_cannot_be_blank(self):
        self.stockAccount.institution_name = ''
        self._assert_stock_is_invalid(self.stockAccount)

    def test_institution_name_cannot_be_none(self):
        self.stockAccount.institution_name = None
        self._assert_stock_is_invalid(self.stockAccount)

    def test_institution_name_can_be_20_characters_long(self):
        self.stockAccount.institution_name = 'a' * 20
        self._assert_stock_is_valid(self.stockAccount)

    def test_institution_name_can_be_1024_characters_long(self):
        self.stockAccount.institution_name = 'a' * 1024
        self._assert_stock_is_valid(self.stockAccount)

    def test_institution_name_cannot_be_1025_characters_long(self):
        self.stockAccount.institution_name = 'a' * 1025
        self._assert_stock_is_invalid(self.stockAccount)

    def test_institution_name_can_contain_numbers(self):
        self.stockAccount.institution_name = '123'
        self._assert_stock_is_valid(self.stockAccount)

    def test_institution_name_can_contain_special_characters(self):
        self.stockAccount.institution_name = '_@*&'
        self._assert_stock_is_valid(self.stockAccount)

    # Tests for Institution ID field

    def test_institution_id_field(self):
        field = StockAccount._meta.get_field('institution_id')
        self.assertIsInstance(field, models.CharField)
        self.assertEqual(field.max_length, 1024)
        self.assertFalse(field.blank)
        self.assertTrue(field.editable)

    def test_institution_id_cannot_be_blank(self):
        self.stockAccount.institution_id = ''
        self._assert_stock_is_invalid(self.stockAccount)

    def test_institution_id_cannot_be_none(self):
        self.stockAccount.institution_id = None
        self._assert_stock_is_invalid(self.stockAccount)

    def test_institution_id_can_be_20_characters_long(self):
        self.stockAccount.institution_id = 'a' * 20
        self._assert_stock_is_valid(self.stockAccount)

    def test_institution_id_can_be_1024_characters_long(self):
        self.stockAccount.institution_id = 'a' * 1024
        self._assert_stock_is_valid(self.stockAccount)

    def test_institution_id_cannot_be_1025_characters_long(self):
        self.stockAccount.institution_id = 'a' * 1025
        self._assert_stock_is_invalid(self.stockAccount)

    def test_institution_id_can_contain_numbers(self):
        self.stockAccount.institution_id = '123'
        self._assert_stock_is_valid(self.stockAccount)

    def test_institution_id_can_contain_special_characters(self):
        self.stockAccount.institution_id = '_@*&'
        self._assert_stock_is_valid(self.stockAccount)

    # Tests for Balance field

    def test_balance_field(self):
        field = StockAccount._meta.get_field('balance')
        self.assertIsInstance(field, MoneyField)
        self.assertEqual(field.default_currency, 'GBP')
        self.assertEqual(field.decimal_places, 2)
        self.assertEqual(field.max_digits, 11)
        self.assertTrue(field.editable)

    def test_balance_cannot_be_none(self):
        self.stockAccount.balance = None
        self._assert_stock_is_invalid(self.stockAccount)

    def test_balance_can_be_zero(self):
        self.stockAccount.balance = Money(0, 'GBP')
        self._assert_stock_is_valid(self.stockAccount)

    def test_balance_can_be_usd(self):
        self.stockAccount.balance = Money(100, 'USD')
        self._assert_stock_is_valid(self.stockAccount)

    def test_balance_can_have_2_decimal_values(self):
        self.stockAccount.balance = Money(99.99, 'GBP')
        self._assert_stock_is_valid(self.stockAccount)

    def test_balance_cannot_have_more_than_2_decimal_values(self):
        self.stockAccount.balance = Money(99.999, 'GBP')
        self._assert_stock_is_invalid(self.stockAccount)

    def test_balance_can_have_11_digits(self):
        self.stockAccount.balance = Money(123456789.00, 'GBP')
        self._assert_stock_is_valid(self.stockAccount)

    def test_balance_cannot_have_more_than_11_digits(self):
        self.stockAccount.balance = Money(112233445566778899.00, 'GBP')
        self._assert_stock_is_invalid(self.stockAccount)

    def test_balance_can_have_invalid_currency(self):
        with self.assertRaises(CurrencyDoesNotExist):
            self.stockAccount.balance = Money(100, 'Gold')
        self._assert_stock_is_valid(self.stockAccount)

    # Tests for Institution Logo field

    def test_institution_logo_field(self):
        field = StockAccount._meta.get_field('institution_logo')
        self.assertIsInstance(field, models.CharField)
        self.assertEqual(field.max_length, 10000)
        self.assertTrue(field.editable)
        self.assertTrue(field.editable)

    def test_institution_logo_cannot_be_none(self):
        self.stockAccount.institution_logo = None
        self._assert_stock_is_invalid(self.stockAccount)

    def test_institution_logo_can_be_20_characters_long(self):
        self.stockAccount.institution_logo = 'a' * 20
        self._assert_stock_is_valid(self.stockAccount)

    def test_institution_logo_can_be_10000_characters_long(self):
        self.stockAccount.institution_logo = 'a' * 10000
        self._assert_stock_is_valid(self.stockAccount)

    def test_institution_logo_cannot_be_10001_characters_long(self):
        self.stockAccount.institution_logo = 'a' * 10001
        self._assert_stock_is_invalid(self.stockAccount)

    def test_institution_logo_can_contain_numbers(self):
        self.stockAccount.institution_logo = '123'
        self._assert_stock_is_valid(self.stockAccount)

    def test_institution_logo_can_contain_special_characters(self):
        self.stockAccount.institution_logo = '_@*&'
        self._assert_stock_is_valid(self.stockAccount)