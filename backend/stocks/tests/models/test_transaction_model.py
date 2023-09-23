from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from stocks.models import Transaction
from django.db import models
# from django.contrib.postgres.fields import ArrayField

class TransactionModelTestCase(TestCase):
    """Tests for transaction model."""

    fixtures = [
        'stocks/tests/fixtures/transaction.json',
        'stocks/tests/fixtures/stocks.json',
        'stocks/tests/fixtures/user.json'
    ]

    def setUp(self):
        self.transaction = Transaction.objects.get(pk="2")
        # self.location = Location.objects.get(pk="1")

    def _assert_transaction_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.transaction.full_clean()
    # account_id field tests

    def test_account_id_is_valid(self):
        field = Transaction._meta.get_field('account_id')
        self.assertIsInstance(field, models.CharField)
        self.assertEqual(field.max_length, 100)
        self.assertFalse(field.blank)
        self.assertFalse(field.null)
    
    def test_account_id_more_than_max_length_not_allowed(self):
        self.transaction.account_id ='a' * 101
        self._assert_transaction_is_invalid()

    def test_account_id_less_than_max_length_is_allowed(self):
        self.transaction.account_id ='a' * 51
        self.assertIsInstance(self.transaction.account_id, str)

    def test_account_id_blank_not_allowed(self):
        self.transaction.account_id = ''
        self._assert_transaction_is_invalid()

    def test_account_id_null_not_allowed(self):
        self.transaction.account_id = None
        self._assert_transaction_is_invalid()

    # amount field tests

    def test_amount_is_valid(self):
        field = Transaction._meta.get_field('amount')
        self.assertIsInstance(field, models.FloatField)
        self.assertFalse(field.blank)
        self.assertFalse(field.null)

    def test_amount_blank_not_allowed(self):
        self.transaction.amount = ''
        self._assert_transaction_is_invalid()

    def test_amount_float_is_valid(self):
        self.transaction.amount = -344.78
        self.assertIsInstance(self.transaction.amount, float)

    def test_amount_null_not_allowed(self):
        self.transaction.amount = None
        self._assert_transaction_is_invalid()
    
    # iso_currency_code field tests

    def test_iso_currency_code_is_valid(self):
        field = Transaction._meta.get_field('iso_currency_code')
        self.assertEqual(field.max_length, 30)
        self.assertIsInstance(field, models.CharField)
        self.assertFalse(field.blank)
        self.assertTrue(field.null)

    def test_iso_currency_code_blank_not_allowed(self):
        self.transaction.iso_currency_code = ''
        self._assert_transaction_is_invalid()

    def test_iso_currency_code_more_than_max_length_not_allowed(self):
        self.transaction.iso_currency_code ='a' * 31
        self._assert_transaction_is_invalid()

    def test_iso_currency_code_less_than_max_length_is_allowed(self):
        self.transaction.iso_currency_code ='a' * 8
        self.assertIsInstance(self.transaction.iso_currency_code, str)

    def test_iso_currency_code_null_allowed(self):
        self.transaction.iso_currency_code = None
        self.assertIsNone(self.transaction.iso_currency_code)

    # unofficial_currency_code field tests

    def test_unofficial_currency_code_is_valid(self):
        field = Transaction._meta.get_field('unofficial_currency_code')
        self.assertEqual(field.max_length, 100)
        self.assertIsInstance(field, models.CharField)
        self.assertFalse(field.blank)
        self.assertTrue(field.null)

    def test_unofficial_currency_code_blank_not_allowed(self):
        self.transaction.unofficial_currency_code = ''
        self._assert_transaction_is_invalid()

    def test_unofficial_currency_code_more_than_max_length_not_allowed(self):
        self.transaction.unofficial_currency_code ='a' * 101
        self._assert_transaction_is_invalid()

    def test_unofficial_currency_code_less_than_max_length_is_allowed(self):
        self.transaction.unofficial_currency_code ='a' * 30
        self.assertIsInstance(self.transaction.unofficial_currency_code, str)

    def test_unofficial_currency_code_null_allowed(self):
        self.transaction.unofficial_currency_code = None
        self.assertIsNone(self.transaction.unofficial_currency_code)

    # date field tests

    def test_date_is_valid(self):
        field = Transaction._meta.get_field('date')
        self.assertIsInstance(field, models.DateField)
        self.assertFalse(field.blank)
        self.assertFalse(field.null)

    def test_date_blank_not_allowed(self):
        self.transaction.date = ''
        self._assert_transaction_is_invalid()

    def test_date_null_not_allowed(self):
        self.transaction.date = None
        self._assert_transaction_is_invalid()
    
    # datetime field tests

    def test_datetime_is_valid(self):
        field = Transaction._meta.get_field('datetime')
        self.assertIsInstance(field, models.DateTimeField)
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    def test_datetime_blank_not_allowed(self):
        self.transaction.datetime = ''
        self._assert_transaction_is_invalid()

    def test_datetime_null_allowed(self):
        self.transaction.datetime = None
        self.assertIsNone(self.transaction.datetime)

    # authorized_date field tests

    def test_authorized_date_is_valid(self):
        field = Transaction._meta.get_field('authorized_date')
        self.assertIsInstance(field, models.DateField)
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    def test_authorized_date_blank_allowed(self):
        self.transaction.authorized_date = ''
        self.assertEqual(self.transaction.authorized_date, '')

    def test_authorized_date_null_allowed(self):
        self.transaction.authorized_date = None
        self.assertIsNone(self.transaction.authorized_date)
    
    # authorized_datetime field tests

    def test_authorized_datetime_is_valid(self):
        field = Transaction._meta.get_field('authorized_datetime')
        self.assertIsInstance(field, models.DateTimeField)
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    def test_authorized_datetime_blank_allowed(self):
        self.transaction.authorized_datetime = ''
        self.assertEqual(self.transaction.authorized_datetime, '')

    def test_authorized_datetime_null_allowed(self):
        self.transaction.authorized_datetime = None
        self.assertIsNone(self.transaction.authorized_datetime)

    # name field tests

    def test_name_is_valid(self):
        field = Transaction._meta.get_field('name')
        self.assertIsInstance(field, models.CharField)
        self.assertEqual(field.max_length, 100)
        self.assertFalse(field.blank)
        self.assertFalse(field.null)
    
    def test_name_more_than_max_length_not_allowed(self):
        self.transaction.account_id ='a' * 51
        self._assert_transaction_is_invalid()

    def test_name_less_than_max_length_is_allowed(self):
        self.transaction.name ='a' * 13
        self.assertIsInstance(self.transaction.name, str)

    def test_name_blank_not_allowed(self):
        self.transaction.name = ''
        self._assert_transaction_is_invalid()

    def test_name_null_not_allowed(self):
        self.transaction.name = None
        self._assert_transaction_is_invalid()
    
    # merchant_name field tests

    def test_merchant_name_is_valid(self):
        field = Transaction._meta.get_field('merchant_name')
        self.assertIsInstance(field, models.CharField)
        self.assertEqual(field.max_length, 50)
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    def test_merchant_name_more_than_max_length_not_allowed(self):
        self.transaction.merchant_name ='a' * 51
        self._assert_transaction_is_invalid()

    def test_merchant_name_less_than_max_length_is_allowed(self):
        self.transaction.merchant_name ='a' * 30
        self.assertIsInstance(self.transaction.merchant_name, str)

    def test_merchant_name_blank_allowed(self):
        self.transaction.merchant_name = ''
        self.assertEqual(self.transaction.merchant_name, '')

    def test_merchant_name_null_allowed(self):
        self.transaction.merchant_name = None
        self.assertIsNone(self.transaction.merchant_name)

    # pending_transaction_id field tests

    def test_pending_transaction_id_is_valid(self):
        field = Transaction._meta.get_field('pending_transaction_id')
        self.assertIsInstance(field, models.CharField)
        self.assertEqual(field.max_length, 100)
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    def test_pending_transaction_id_more_than_max_length_not_allowed(self):
        self.transaction.pending_transaction_id ='a' * 101
        self._assert_transaction_is_invalid()

    def test_pending_transaction_id_less_than_max_length_is_allowed(self):
        self.transaction.pending_transaction_id ='a' * 30
        self.assertIsInstance(self.transaction.pending_transaction_id, str)

    def test_pending_transaction_id_blank_allowed(self):
        self.transaction.pending_transaction_id = ''
        self.assertEqual(self.transaction.pending_transaction_id, '')

    def test_pending_transaction_id_null_allowed(self):
        self.transaction.pending_transaction_id = None
        self.assertIsNone(self.transaction.pending_transaction_id)

    # account_owner field tests

    def test_account_owner_is_valid(self):
        field = Transaction._meta.get_field('account_owner')
        self.assertIsInstance(field, models.CharField)
        self.assertEqual(field.max_length, 50)
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    def test_account_owner_more_than_max_length_not_allowed(self):
        self.transaction.account_owner ='a' * 51
        self._assert_transaction_is_invalid()

    def test_account_owner_less_than_max_length_is_allowed(self):
        self.transaction.account_owner ='a' * 30
        self.assertIsInstance(self.transaction.account_owner, str)

    def test_account_owner_blank_allowed(self):
        self.transaction.account_owner = ''
        self.assertEqual(self.transaction.account_owner, '')

    def test_account_owner_null_allowed(self):
        self.transaction.account_owner = None
        self.assertIsNone(self.transaction.account_owner)

    # transaction_code field tests

    def test_transaction_code_is_valid(self):
        field = Transaction._meta.get_field('transaction_code')
        self.assertIsInstance(field, models.CharField)
        self.assertEqual(field.max_length, 30)
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    def test_transaction_code_more_than_max_length_not_allowed(self):
        self.transaction.transaction_code ='a' * 31
        self._assert_transaction_is_invalid()

    def test_transaction_code_less_than_max_length_is_allowed(self):
        self.transaction.transaction_code ='a' * 8
        self.assertIsInstance(self.transaction.transaction_code, str)

    def test_transaction_code_blank_allowed(self):
        self.transaction.transaction_code = ''
        self.assertEqual(self.transaction.transaction_code, '')

    def test_transaction_code_null_allowed(self):
        self.transaction.transaction_code = None
        self.assertIsNone(self.transaction.transaction_code)

    def test_transaction_code_valid_choice(self):
        self.transaction.transaction_code = "adjustment"
        self.assertIsInstance(self.transaction.transaction_code, str)

    def test_transaction_code_valid_choice_2(self):
        self.transaction.transaction_code = "cashback"
        self.assertIsInstance(self.transaction.transaction_code, str)

    def test_transaction_code_valid_choice_3(self):
        self.transaction.transaction_code = "standing order"
        self.assertIsInstance(self.transaction.transaction_code, str)

    def test_transaction_code_invalid_choice(self):
        self.transaction.transaction_code = "invalid choice"
        self._assert_transaction_is_invalid()

    def test_latitude_field(self):
        field = Transaction._meta.get_field('latitude')
        self.assertIsInstance(field, models.FloatField)
        self.assertFalse(field.null)
        self.assertFalse(field.blank)

    def test_latitude_cannot_be_blank(self):
        self.transaction.latitude = ''
        self._assert_transaction_is_invalid()
    
    def test_latitude_cannot_be_none(self):
        self.transaction.latitude = None
        self._assert_transaction_is_invalid()

    def test_decimal_latitude(self):
        self.transaction.latitude = 0.5
        self.assertIsInstance(self.transaction.latitude, float)

    def test_integer_latitude(self):
        self.transaction.latitude = 1
        self.assertIsInstance(self.transaction.latitude, int)

    def test_longitude_field(self):
        field = Transaction._meta.get_field('longitude')
        self.assertIsInstance(field, models.FloatField)
        self.assertFalse(field.null)
        self.assertFalse(field.blank)

    def test_longitude_cannot_be_blank(self):
        self.transaction.longitude = ''
        self._assert_transaction_is_invalid()
    
    def test_longitude_cannot_be_none(self):
        self.transaction.longitude = None
        self._assert_transaction_is_invalid()

    def test_decimal_longitude(self):
        self.transaction.longitude = 0.5
        self.assertIsInstance(self.transaction.latitude, float)

    def test_integer_longitude(self):
        self.transaction.longitude = 1
        self.assertIsInstance(self.transaction.longitude, int)
