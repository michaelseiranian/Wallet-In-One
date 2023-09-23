from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from accounts.models import User
from rest_framework.exceptions import ErrorDetail
from stocks.models import StockAccount


""" Tests for Listing all Stock Accounts for a specified user """
class ListStockAccountViewTestCase(TestCase):
    fixtures = [
        'stocks/tests/fixtures/user.json',
        'stocks/tests/fixtures/stocks.json'
    ]

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.get(id=3)  
        self.client.force_authenticate(self.user)
        self.url = reverse('list_accounts')

    def test_url(self):
        self.assertEqual(self.url,'/stocks/list_accounts/')

    def test_successful_list_accounts(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(len(response.data), len(StockAccount.objects.filter(user=self.user)))

    def test_unsuccessful_list_accounts(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.data['detail'],  ErrorDetail(string='Method "POST" not allowed.', code='method_not_allowed'))
        self.assertEqual(len(response.data), 1)

    def test_no_accounts(self):
        user = User.objects.get(id=1)
        self.client.force_authenticate(user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)
        self.assertEqual(len(response.data), len(StockAccount.objects.filter(user=user)))