from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from accounts.models import User
from stocks.models import StockAccount, Stock


""" Tests for Adding a Stock View """
class AddStockViewTestCase(TestCase):
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
            'name': 'Test Stock View',
            'quantity': 10,
            'stockAccount': self.stockAccount.account_id,
            'ticker_symbol': 'TEST',
            'institution_price': 100,
            'security_id': '123'
        }
        self.url = reverse('add_stock')

    def test_url(self):
        self.assertEqual(self.url,'/stocks/add_stock/')

    def test_successful_add_stock(self):
        before = len(Stock.objects.all())
        response = self.client.post(self.url, data=self.serializer_input)
        after = len(Stock.objects.all())
        self.assertEqual(before+1,after)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Stock.objects.filter(name='Test Stock View').count(), 1)

    def test_unsuccessful_add_stock(self):
        self.serializer_input['name'] = ''
        before = len(Stock.objects.all())
        response = self.client.post(self.url, data=self.serializer_input)
        after = len(Stock.objects.all())
        self.assertEqual(before,after)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Stock.objects.filter(name='Test Stock View').count(), 0)
