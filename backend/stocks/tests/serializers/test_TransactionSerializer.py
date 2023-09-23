import datetime
import zoneinfo
from rest_framework.test import APIRequestFactory, APIClient
from stocks.serializers import AddTransaction
from stocks.models import StockAccount
from accounts.models import User
from django.test import TestCase
from rest_framework.exceptions import ErrorDetail


""" Unit Tests for Transaction Serializer """
class TransactionSerializerTestCase(TestCase):
    fixtures = [
        'stocks/tests/fixtures/stocks.json',
        'stocks/tests/fixtures/user.json'
    ]

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.get(pk='3')
        self.client.force_authenticate(self.user)
        self.stockAccount = StockAccount.objects.get(account_id="1")
        self.serializer_input = {
            'account_id': '123',
            'amount': 10,
            'quantity': 100,
            'price': 20,
            'fees': 5,
            "iso_currency_code": "USD",
            "unofficial_currency_code": None,
            "date": "2017-01-29",
            "datetime": "2017-01-27T11:00:00Z",
            "authorized_date": "2017-01-27",
            "authorized_datetime": "2017-01-27T10:34:50Z",
            "name": "Apple Store",
            "merchant_name": "Apple",
            'stock': self.stockAccount.account_id,
            "pending_transaction_id": None,
            "account_owner": None,
            "transaction_code": None,
            "investment_transaction_id": "Test Transaction",
            "security_id": "Test ID",
            "latitude": 35.5,
            "longitude": 77
        }

    def initiate_serializer(self):
        factory = APIRequestFactory()
        request = factory.post('/')
        request.user = self.user
        serializer = AddTransaction(data=self.serializer_input, context={'request': request})
        return serializer
    
    def test_serializer(self):
        serializer = self.initiate_serializer()
        self.assertTrue(serializer.is_valid())

    def test_fields(self):
        serializer = self.initiate_serializer()
        self.assertTrue(serializer.is_valid())
        data = serializer.data
        self.assertCountEqual(data.keys(), set(['account_id', 'amount', 'name', 'quantity', 'price', 'fees', 'iso_currency_code', 'unofficial_currency_code', 'date', 'datetime', 'authorized_date', 'authorized_datetime', 'merchant_name', 'stock', 'pending_transaction_id', 'account_owner', 'transaction_code', 'investment_transaction_id', 'security_id', 'latitude', 'longitude']))

    def test_invalid_account_id(self):
        self.serializer_input['account_id'] = ''
        serializer = self.initiate_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['account_id']))
        self.assertTrue(serializer.errors == {'account_id': [ErrorDetail(string='This field may not be blank.', code='blank')]})

    def test_invalid_amount(self):
        self.serializer_input['amount'] = None
        serializer = self.initiate_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['amount']))
        self.assertTrue(serializer.errors == {'amount': [ErrorDetail(string='This field may not be null.', code='null')]})

    def test_invalid_quantity(self):
        self.serializer_input['quantity'] = None
        serializer = self.initiate_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['quantity']))
        self.assertTrue(serializer.errors == {'quantity': [ErrorDetail(string='This field may not be null.', code='null')]})

    def test_invalid_price(self):
        self.serializer_input['price'] = None
        serializer = self.initiate_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['price']))
        self.assertTrue(serializer.errors == {'price': [ErrorDetail(string='This field may not be null.', code='null')]})

    def test_invalid_fees(self):
        self.serializer_input['fees'] = 'Wrong Type'
        serializer = self.initiate_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['fees']))
        self.assertTrue(serializer.errors == {'fees': [ErrorDetail(string='A valid number is required.', code='invalid')]})

    def test_invalid_iso_currency_code(self):
        self.serializer_input['iso_currency_code'] = 'a' * 31
        serializer = self.initiate_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['iso_currency_code']))
        self.assertTrue(serializer.errors == {'iso_currency_code': [ErrorDetail(string='Ensure this field has no more than 30 characters.', code='max_length')]})

    def test_invalid_unofficial_currency_code(self):
        self.serializer_input['unofficial_currency_code'] = 'a' * 101
        serializer = self.initiate_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['unofficial_currency_code']))
        self.assertTrue(serializer.errors == {'unofficial_currency_code': [ErrorDetail(string='Ensure this field has no more than 100 characters.', code='max_length')]})

    def test_invalid_date(self):
        self.serializer_input['date'] = None
        serializer = self.initiate_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['date']))
        self.assertTrue(serializer.errors == {'date': [ErrorDetail(string='This field may not be null.', code='null')]})

    def test_invalid_datetime(self):
        self.serializer_input['datetime'] = 1
        serializer = self.initiate_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['datetime']))
        self.assertTrue(serializer.errors == {'datetime': [ErrorDetail(string='Datetime has wrong format. Use one of these formats instead: YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z].', code='invalid')]})

    def test_invalid_authorized_date(self):
        self.serializer_input['authorized_date'] = 1
        serializer = self.initiate_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['authorized_date']))
        self.assertTrue(serializer.errors == {'authorized_date': [ErrorDetail(string='Date has wrong format. Use one of these formats instead: YYYY-MM-DD.', code='invalid')]})

    def test_invalid_authorized_datetime(self):
        self.serializer_input['authorized_datetime'] = 1
        serializer = self.initiate_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['authorized_datetime']))
        self.assertTrue(serializer.errors == {'authorized_datetime': [ErrorDetail(string='Datetime has wrong format. Use one of these formats instead: YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z].', code='invalid')]})

    def test_invalid_name(self):
        self.serializer_input['name'] = ''
        serializer = self.initiate_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['name']))
        self.assertTrue(serializer.errors == {'name': [ErrorDetail(string='This field may not be blank.', code='blank')]})

    def test_invalid_merchant_name(self):
        self.serializer_input['merchant_name'] = 'a' * 101
        serializer = self.initiate_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['merchant_name']))
        self.assertTrue(serializer.errors == {'merchant_name': [ErrorDetail(string='Ensure this field has no more than 50 characters.', code='max_length')]})

    def test_invalid_pending_transaction_id(self):
        self.serializer_input['pending_transaction_id'] = 'a' * 101
        serializer = self.initiate_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['pending_transaction_id']))
        self.assertTrue(serializer.errors == {'pending_transaction_id': [ErrorDetail(string='Ensure this field has no more than 100 characters.', code='max_length')]})

    def test_invalid_account_owner(self):
        self.serializer_input['account_owner'] = 'a' * 101
        serializer = self.initiate_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['account_owner']))
        self.assertTrue(serializer.errors == {'account_owner': [ErrorDetail(string='Ensure this field has no more than 50 characters.', code='max_length')]})

    def test_invalid_investment_transaction_id(self):
        self.serializer_input['investment_transaction_id'] = ''
        serializer = self.initiate_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['investment_transaction_id']))
        self.assertTrue(serializer.errors == {'investment_transaction_id': [ErrorDetail(string='This field may not be blank.', code='blank')]})

    def test_invalid_security_id(self):
        self.serializer_input['security_id'] = ''
        serializer = self.initiate_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['security_id']))
        self.assertTrue(serializer.errors == {'security_id': [ErrorDetail(string='This field may not be blank.', code='blank')]})

    def test_invalid_transaction_code(self):
        self.serializer_input['transaction_code'] = 'a'
        serializer = self.initiate_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['transaction_code']))
        self.assertTrue(serializer.errors == {'transaction_code': [ErrorDetail(string='"a" is not a valid choice.', code='invalid_choice')]})

    def test_serializer_cannot_be_empty(self):
        self.serializer_input = ''
        serializer = self.initiate_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertTrue(serializer.errors == {'non_field_errors': [ErrorDetail(string='Invalid data. Expected a dictionary, but got str.', code='invalid')]})

    def test_serializer_cannot_be_none(self):
        self.serializer_input = None
        serializer = self.initiate_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertTrue(serializer.errors == {'non_field_errors': [ErrorDetail(string='No data provided', code='null')]})

    def test_invalid_latitude(self):
        self.serializer_input['latitude'] = None
        serializer = self.initiate_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['latitude']))
        self.assertTrue(serializer.errors == {'latitude': [ErrorDetail(string='This field may not be null.', code='null')]})

    def test_invalid_longitude(self):
        self.serializer_input['longitude'] = None
        serializer = self.initiate_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['longitude']))
        self.assertTrue(serializer.errors == {'longitude': [ErrorDetail(string='This field may not be null.', code='null')]})

    def test_validated_data(self):
        serializer = self.initiate_serializer()
        self.assertTrue(serializer.is_valid())
        self.assertTrue(serializer.validated_data == {
            'account_id': '123',
            'amount': 10,
            'quantity': 100,
            'price': 20,
            'fees': 5,
            "iso_currency_code": "USD",
            "unofficial_currency_code": None,
            "date": datetime.date(2017, 1, 29),
            "datetime": datetime.datetime(2017, 1, 27, 11, 0, tzinfo=zoneinfo.ZoneInfo(key='UTC')),
            "authorized_date": datetime.date(2017, 1, 27),
            "authorized_datetime": datetime.datetime(2017, 1, 27, 10, 34, 50, tzinfo=zoneinfo.ZoneInfo(key='UTC')),
            "name": "Apple Store",
            "merchant_name": "Apple",
            'stock': self.stockAccount,
            "pending_transaction_id": None,
            "account_owner": None,
            "transaction_code": None,
            "investment_transaction_id": "Test Transaction",
            "security_id": "Test ID",
            "latitude": 35.5,
            "longitude": 77
        })
        self.assertTrue(serializer.errors == {})



        