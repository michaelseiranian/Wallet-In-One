from django.test import TestCase
from stocks.models import Stock, StockAccount
from django.core.exceptions import ValidationError
from django.db import models
from djmoney.models.fields import MoneyField
from djmoney.money import Money
from moneyed.classes import CurrencyDoesNotExist

""" Unit Tests for the Stock Model """
class StockModelTestCase(TestCase):

    fixtures = [
        'stocks/tests/fixtures/stocks.json',
        'stocks/tests/fixtures/user.json',
    ]

    def setUp(self):
        self.stock = Stock.objects.get(pk=1)

    def _assert_stock_is_valid(self, stock):
        try:
            stock.full_clean()
        except ValidationError:
            self.fail("Stock Account is not valid.")

    def _assert_stock_is_invalid(self, stock):
        with self.assertRaises(ValidationError):
            stock.full_clean()

    def test_stock_is_valid(self):
        self._assert_stock_is_valid(self.stock)

    # Tests for Stock Account Foreign Key Field

    def test_stock_account_foreign_key_field(self):
        field = Stock._meta.get_field('stockAccount')
        self.assertIsInstance(field, models.ForeignKey)
        self.assertEqual(field.many_to_one, True)
        self.assertFalse(field.blank)

    def test_user_on_delete_cascade(self):
        stockAccount = StockAccount.objects.get(account_id="1")
        stockAccount.delete()
        self.assertFalse(Stock.objects.filter(pk=1).exists())

    # Tests for Name field

    def test_name_field(self):
        field = Stock._meta.get_field('name')
        self.assertIsInstance(field, models.CharField)
        self.assertEqual(field.max_length, 1024)
        self.assertFalse(field.blank)

    def test_name_cannot_be_blank(self):
        self.stock.name = ''
        self._assert_stock_is_invalid(self.stock)

    def test_name_cannot_be_none(self):
        self.stock.name = None
        self._assert_stock_is_invalid(self.stock)

    def test_name_can_be_20_characters(self):
        self.stock.name = 'a' * 20
        self._assert_stock_is_valid(self.stock)

    def test_name_can_be_1024_characters(self):
        self.stock.name = 'a' * 1024
        self._assert_stock_is_valid(self.stock)

    def test_name_cannot_be_1025_characters(self):
        self.stock.name = 'a' * 1025
        self._assert_stock_is_invalid(self.stock)

    def test_name_can_contain_numbers(self):
        self.stock.name = '123'
        self._assert_stock_is_valid(self.stock)

    def test_name_can_contain_special_characters(self):
        self.stock.name = '_@*&'
        self._assert_stock_is_valid(self.stock)

    # Tests for Ticker Symbol field

    def test_ticker_symbol_field(self):
        field = Stock._meta.get_field('ticker_symbol')
        self.assertIsInstance(field, models.CharField)
        self.assertEqual(field.max_length, 1024)
        self.assertFalse(field.blank)

    def test_ticker_symbol_cannot_be_blank(self):
        self.stock.ticker_symbol = ''
        self._assert_stock_is_invalid(self.stock)

    def test_ticker_symbol_cannot_be_none(self):
        self.stock.ticker_symbol = None
        self._assert_stock_is_invalid(self.stock)

    def test_ticker_symbol_can_be_20_characters(self):
        self.stock.ticker_symbol = 'a' * 20
        self._assert_stock_is_valid(self.stock)

    def test_ticker_symbol_can_be_1024_characters(self):
        self.stock.ticker_symbol = 'a' * 1024
        self._assert_stock_is_valid(self.stock)

    def test_ticker_symbol_cannot_be_1025_characters(self):
        self.stock.ticker_symbol = 'a' * 1025
        self._assert_stock_is_invalid(self.stock)

    def test_ticker_symbol_can_contain_numbers(self):
        self.stock.ticker_symbol = '123'
        self._assert_stock_is_valid(self.stock)

    def test_ticker_symbol_can_contain_special_characters(self):
        self.stock.ticker_symbol = '_@*&'
        self._assert_stock_is_valid(self.stock)

    # Tests for Quantity field

    def test_quantity_field(self):
        field = Stock._meta.get_field('quantity')
        self.assertIsInstance(field, models.FloatField)
        self.assertFalse(field.null)
        self.assertFalse(field.blank)

    def test_quantity_cannot_be_blank(self):
        self.stock.quantity = ''
        self._assert_stock_is_invalid(self.stock)
    
    def test_quantity_cannot_be_none(self):
        self.stock.quantity = None
        self._assert_stock_is_invalid(self.stock)

    def test_decimal_quantity(self):
        self.stock.quantity = 0.5
        self._assert_stock_is_valid(self.stock)

    def test_integer_quantity(self):
        self.stock.quantity = 1
        self._assert_stock_is_valid(self.stock)

    # Tests for Institution Price field

    def test_institution_price_field(self):
        field = Stock._meta.get_field('institution_price')
        self.assertIsInstance(field, MoneyField)
        self.assertEqual(field.default_currency, 'GBP')
        self.assertEqual(field.decimal_places, 2)
        self.assertEqual(field.max_digits, 11)
        self.assertTrue(field.editable)

    def test_institution_price_cannot_be_none(self):
        self.stock.institution_price = None
        self._assert_stock_is_invalid(self.stock)

    def test_institution_price_can_be_zero(self):
        self.stock.institution_price = 0
        self._assert_stock_is_valid(self.stock)

    def test_institution_price_can_be_usd(self):
        self.stock.institution_price = Money(100, 'USD')
        self._assert_stock_is_valid(self.stock)

    def test_institution_price_can_have_2_decimal_places(self):
        self.stock.institution_price = Money(99.99, 'GBP')
        self._assert_stock_is_valid(self.stock)

    def test_institution_price_cannot_have_more_than_2_decimal_places(self):
        self.stock.institution_price = Money(99.999, 'GBP')
        self._assert_stock_is_invalid(self.stock)

    def test_institution_price_can_have_11_digits(self):
        self.stock.institution_price = Money(123456789.00, 'GBP')
        self._assert_stock_is_valid(self.stock)

    def test_institution_price_cannot_have_more_than_11_digits(self):
        self.stock.institution_price = Money(112233445566778899.00, 'GBP')
        self._assert_stock_is_invalid(self.stock)

    def test_institution_price_can_have_invalid_currency(self):
        with self.assertRaises(CurrencyDoesNotExist):
            self.stock.institution_price = Money(100, 'Gold')
        self._assert_stock_is_valid(self.stock)

    # Tests for Security ID field

    def test_security_id_field(self):
        field = Stock._meta.get_field('security_id')
        self.assertIsInstance(field, models.CharField)
        self.assertEqual(field.max_length, 100)
        self.assertFalse(field.blank)

    def test_security_id_cannot_be_blank(self):
        self.stock.security_id = ''
        self._assert_stock_is_invalid(self.stock)

    def test_security_id_cannot_be_none(self):
        self.stock.security_id = None
        self._assert_stock_is_invalid(self.stock)

    def test_security_id_can_be_20_characters(self):
        self.stock.security_id = 'a' * 20
        self._assert_stock_is_valid(self.stock)

    def test_security_id_can_be_100_characters(self):
        self.stock.security_id = 'a' * 100
        self._assert_stock_is_valid(self.stock)

    def test_security_id_cannot_be_101_characters(self):
        self.stock.security_id = 'a' * 101
        self._assert_stock_is_invalid(self.stock)

    def test_security_id_can_contain_numbers(self):
        self.stock.security_id = '123'
        self._assert_stock_is_valid(self.stock)

    def test_security_id_can_contain_special_characters(self):
        self.stock.security_id = '_@*&'
        self._assert_stock_is_valid(self.stock)