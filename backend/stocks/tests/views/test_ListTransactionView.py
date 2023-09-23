from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from accounts.models import User
from rest_framework.exceptions import ErrorDetail
from stocks.models import Transaction

""" Tests for Listing all Transactions for a specified user """
class ListTransactionViewTestCase(TestCase):
    fixtures = [
        'stocks/tests/fixtures/user.json',
        'stocks/tests/fixtures/stocks.json',
        'stocks/tests/fixtures/transaction.json'
    ]

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.get(id=3)  
        self.client.force_authenticate(self.user)
        self.url = reverse('list_transactions',kwargs={'stock':'1'})

    def test_url(self):
        self.assertEqual(self.url,'/stocks/list_transactions/1/')

    def test_successful_list_transactions(self):
        self.url = reverse('list_transactions',kwargs={'stock':'1'})
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(len(response.data), len(Transaction.objects.filter(stock='1', stock__user=self.user)))

    def test_unsuccessful_list_transactions(self):
        self.url = reverse('list_transactions',kwargs={'stock':'1'})
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.data['detail'],  ErrorDetail(string='Method "POST" not allowed.', code='method_not_allowed'))
        self.assertEqual(len(response.data), 1)

    def test_no_transactions(self):
        user = User.objects.get(id=1)
        self.client.force_authenticate(user)
        self.url = reverse('list_transactions',kwargs={'stock':'1'})
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)
        self.assertEqual(len(response.data), len(Transaction.objects.filter(stock='1', stock__user=user)))

    def test_invalid_transactions(self):
        self.url = reverse('list_transactions',kwargs={'stock':'INVALID_ACCOUNT'})
        response = self.client.get(self.url)
        self.assertEquals(len(response.data),0)

    def test_user_cannot_see_transactions_in_other_users_account(self):
        self.user = User.objects.get(id=1) 
        self.client.force_authenticate(self.user)
        self.url = reverse('list_transactions',kwargs={'stock':'1'})
        response = self.client.get(self.url)
        self.assertEquals(len(response.data),0)
        self.assertEqual(len(response.data), len(Transaction.objects.filter(stock='1', stock__user=self.user)))