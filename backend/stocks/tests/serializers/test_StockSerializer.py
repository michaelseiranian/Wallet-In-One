from rest_framework.test import APIRequestFactory, APIClient
from stocks.serializers import AddStock
from stocks.models import StockAccount
from accounts.models import User
from django.test import TestCase
from djmoney.money import Money
from rest_framework.exceptions import ErrorDetail


""" Unit Tests for Stock Serializer """
class StockSerializerTestCase(TestCase):
    fixtures = [
        'stocks/tests/fixtures/stocks.json',
        'stocks/tests/fixtures/user.json',
    ]

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.get(pk='3')
        self.client.force_authenticate(self.user)
        self.stockAccount = StockAccount.objects.get(account_id="1")
        self.serializer_input = {
            'name': 'Test Stock',
            'quantity': 10,
            'stockAccount': self.stockAccount.account_id,
            'ticker_symbol': 'TEST',
            'institution_price': Money(100, 'GBP'),
            'security_id': '123'
        }


    def initiate_serializer(self):
        factory = APIRequestFactory()
        request = factory.post('/')
        request.user = self.user
        serializer = AddStock(data=self.serializer_input, context={'request': request})
        return serializer
    
    def test_serializer(self):
        serializer = self.initiate_serializer()
        self.assertTrue(serializer.is_valid())


    def test_fields(self):
        serializer = self.initiate_serializer()
        self.assertTrue(serializer.is_valid())
        data = serializer.data
        self.assertCountEqual(data.keys(), set(['name', 'quantity', 'stockAccount', 'ticker_symbol', 'institution_price', 'security_id']))

    def test_invalid_name(self):
        self.serializer_input['name'] = ''
        serializer = self.initiate_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['name']))
        self.assertTrue(serializer.errors == {'name': [ErrorDetail(string='This field may not be blank.', code='blank')]})

    def test_invalid_ticker_symbol(self):
        self.serializer_input['ticker_symbol'] = ''
        serializer = self.initiate_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['ticker_symbol']))
        self.assertTrue(serializer.errors == {'ticker_symbol': [ErrorDetail(string='This field may not be blank.', code='blank')]})

    def test_invalid_quantity(self):
        self.serializer_input['quantity'] = None
        serializer = self.initiate_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['quantity']))
        self.assertTrue(serializer.errors == {'quantity': [ErrorDetail(string='This field may not be null.', code='null')]})

    def test_invalid_institution_price(self):
        self.serializer_input['institution_price'] = None
        serializer = self.initiate_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['institution_price']))
        self.assertTrue(serializer.errors == {'institution_price': [ErrorDetail(string='This field may not be null.', code='null')]})

    def test_invalid_stock_account(self):
        self.serializer_input['stockAccount'] = "123456789"
        serializer = self.initiate_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['stockAccount']))
        self.assertTrue(serializer.errors == {'stockAccount': [ErrorDetail(string='Invalid pk "123456789" - object does not exist.', code='does_not_exist')]})

    def test_invalid_security_id(self):
        self.serializer_input['security_id'] = ''
        serializer = self.initiate_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['security_id']))
        self.assertTrue(serializer.errors == {'security_id': [ErrorDetail(string='This field may not be blank.', code='blank')]})

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

    def test_validated_data(self):
        serializer = self.initiate_serializer()
        self.assertTrue(serializer.is_valid())
        self.assertTrue(serializer.validated_data == {
            'name': 'Test Stock',
            'quantity': 10,
            'stockAccount': self.stockAccount,
            'ticker_symbol': 'TEST',
            'institution_price': Money(100, 'GBP'),
            'security_id': '123'
        })
        self.assertTrue(serializer.errors == {})

    def test_institution_price_saves_correctly_as_money_field(self):
        self.serializer_input['institution_price'] = 10
        serializer = self.initiate_serializer()
        self.assertTrue(serializer.is_valid())
        account = serializer.save()
        account.refresh_from_db()
        self.assertEqual(account.institution_price, Money(10, 'GBP'))
        self.assertTrue(serializer.errors == {})
