from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from accounts.models import User
from stocks.models import StockAccount, Transaction


""" Tests for Adding a Transaction View """
class AddTransactionViewTestCase(TestCase):
    fixtures = [
        'stocks/tests/fixtures/user.json',
        'stocks/tests/fixtures/stocks.json'
    ]

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.get(id=3)  
        self.client.force_authenticate(self.user)
        self.stockAccount = StockAccount.objects.get(account_id="1")
        self.serializer_input = {
            'account_id': '123',
            'amount': 10,
            'quantity': 100,
            'price': 20,
            'fees': 5,
            "iso_currency_code": "USD",
            "unofficial_currency_code": '',
            "date": "2017-01-29",
            "datetime": "2017-01-27T11:00:00Z",
            "authorized_date": "2017-01-27",
            "authorized_datetime": "2017-01-27T10:34:50Z",
            "name": "Apple Store",
            "merchant_name": "Apple",
            'stock': self.stockAccount.account_id,
            "pending_transaction_id": '',
            "account_owner": '',
            "transaction_code": '',
            "investment_transaction_id": "Test Transaction",
            "security_id": "Test ID",
            "latitude": 35.5,
            "longitude": 77
        }
        self.url = reverse('add_transaction_account')

    def test_url(self):
        self.assertEqual(self.url,'/stocks/add_transaction_account/')

    def test_successful_add_transaction(self):
        before = len(Transaction.objects.all())
        response = self.client.post(self.url, data=self.serializer_input)
        after = len(Transaction.objects.all())
        self.assertEqual(before+1,after)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Transaction.objects.filter(name='Apple Store').count(), 1)

    def test_unsuccessful_add_transaction(self):
        self.serializer_input['name'] = ''
        before = len(Transaction.objects.all())
        response = self.client.post(self.url, data=self.serializer_input)
        after = len(Transaction.objects.all())
        self.assertEqual(before,after)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Transaction.objects.filter(name='Apple Store').count(), 0)