from django.test import TestCase, Client
from rest_framework.test import APIClient
from django.urls import reverse
from accounts.models import User
from rest_framework import status
from stocks.models import StockAccount


""" Tests for Deleting a Stock Account """
class DeleteStockAccountViewTestCase(TestCase):
    fixtures = [
        'stocks/tests/fixtures/user.json',
        'stocks/tests/fixtures/stocks.json'
    ]

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.get(id=3)  
        self.client.force_authenticate(self.user)

    def test_url(self):
        self.url = reverse('delete_account_stocks', kwargs={'stockAccount':'1'})
        self.assertEqual(self.url,'/stocks/delete_account/1/')

    def test_delete_account(self):
        before = len(StockAccount.objects.filter(user=self.user))
        self.url = reverse('delete_account_stocks', kwargs={'stockAccount':'1'})
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        after = len(StockAccount.objects.filter(user=self.user))
        self.assertEqual(before-1,after)    # Should have 1 less Stock Account for the Logged In User

    def test_delete_invalid_account(self):
        before = len(StockAccount.objects.filter(user=self.user))
        self.url = reverse('delete_account_stocks', kwargs={'stockAccount':'INVALID_ID'})
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        after = len(StockAccount.objects.filter(user=self.user))
        self.assertEqual(before,after) # Should have the same number of accounts

    def test_user_cannot_delete_another_users_account(self):
        self.url = reverse('delete_account_stocks', kwargs={'stockAccount':'1'})
        self.user = User.objects.get(id=1) 
        self.client.force_authenticate(self.user)
        before = len(StockAccount.objects.filter(user=self.user))
        self.client.delete(self.url)
        after = len(StockAccount.objects.filter(user=self.user))
        self.assertEqual(before,after) # Should have the same number of accounts