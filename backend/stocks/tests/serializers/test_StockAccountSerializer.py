from rest_framework.test import APIRequestFactory, APIClient
from stocks.serializers import AddStockAccount
from stocks.models import StockAccount
from rest_framework.request import Request
from djmoney.money import Money
from accounts.models import User
from django.test import TestCase
from rest_framework.exceptions import ErrorDetail


""" Unit Tests for Stock Account Serializer """
class StockAccountSerializerTestCase(TestCase):

    fixtures = [
        'stocks/tests/fixtures/stocks.json',
        'stocks/tests/fixtures/user.json',
    ]

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.get(pk='3')
        self.client.force_authenticate(self.user)
        self.serializer_input = {
            'account_id': '10',
            'access_token': 'Test Access Token',
            'name': 'Test Stock Account',
            'institution_id': 'ins_1',
            'institution_name': 'Test Institution Name',
            'institution_logo': 'Test Logo',
            'balance': Money(100, 'GBP')
        }
        
    def initiate_serializer(self):
        factory = APIRequestFactory()
        request = factory.post('/')
        request.user = self.user
        serializer = AddStockAccount(data=self.serializer_input, context={'request': request})
        return serializer

    def test_serializer(self):
        serializer = self.initiate_serializer()
        self.assertTrue(serializer.is_valid())

    def test_fields(self):
        serializer = self.initiate_serializer()
        self.assertTrue(serializer.is_valid())
        data = serializer.data
        self.assertCountEqual(data.keys(), set(['account_id', 'access_token', 'name', 'institution_id', 'institution_name', 'institution_logo', 'balance']))

    def test_invalid_account_id(self):
        self.serializer_input['account_id'] = ''
        serializer = self.initiate_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['account_id']))
        self.assertTrue(serializer.errors == {'account_id': [ErrorDetail(string='This field may not be blank.', code='blank')]})

    def test_invalid_access_token(self):
        self.serializer_input['access_token'] = ''
        serializer = self.initiate_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['access_token']))
        self.assertTrue(serializer.errors == {'access_token': [ErrorDetail(string='This field may not be blank.', code='blank')]})

    def test_invalid_name(self):
        self.serializer_input['name'] = ''
        serializer = self.initiate_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['name']))
        self.assertTrue(serializer.errors == {'name': [ErrorDetail(string='This field may not be blank.', code='blank')]})

    def test_invalid_institution_id(self):
        self.serializer_input['institution_id'] = ''
        serializer = self.initiate_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['institution_id']))
        self.assertTrue(serializer.errors == {'institution_id': [ErrorDetail(string='This field may not be blank.', code='blank')]})

    def test_invalid_institution_logo(self):
        self.serializer_input['institution_logo'] = 'a' * 10001
        serializer = self.initiate_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['institution_logo']))
        self.assertTrue(serializer.errors == {'institution_logo': [ErrorDetail(string='Ensure this field has no more than 10000 characters.', code='max_length')]})

    def test_invalid_balance(self):
        self.serializer_input['balance'] = None
        serializer = self.initiate_serializer()
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['balance']))
        self.assertTrue(serializer.errors == {'balance': [ErrorDetail(string='This field may not be null.', code='null')]})

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
            'account_id': '10',
            'access_token': 'Test Access Token',
            'name': 'Test Stock Account',
            'user': self.user,
            'institution_id': 'ins_1',
            'institution_name': 'Test Institution Name',
            'institution_logo': 'Test Logo',
            'balance': Money(100, 'GBP')
        })
        self.assertTrue(serializer.errors == {})

    def test_balance_saves_correctly_as_money_field(self):
        self.serializer_input['balance'] = 10
        serializer = self.initiate_serializer()
        self.assertTrue(serializer.is_valid())
        account = serializer.save()
        account.refresh_from_db()
        self.assertEqual(account.balance, Money(10, 'GBP'))
        self.assertTrue(serializer.errors == {})

    def test_account_already_exists(self):
        self.serializer_input['name'] = 'Test Stock Account'
        self.serializer_input['institution_id'] = '1'
        serializer = self.initiate_serializer()
        self.assertFalse(serializer.is_valid())