from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from django.urls import reverse
from accounts.models import User
from banking.models import Account, Transaction
from rest_framework import status

class TransactionViewTestCase(TestCase):
    
    fixtures = [
        'accounts/fixtures/user.json',
        'banking/tests/fixtures/bank_data.json'
    ]

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.get(id=1) 

        # Test the data stored in the database
        for a in Account.objects.filter(user=self.user):
            a.last_update = timezone.now()
            a.save()

        self.client.force_authenticate(self.user)
        self.url = reverse('transactions')

    def test_url(self):
        self.assertEqual(self.url,'/banking/transactions/')

    def test_response_from_all_accounts_from_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data),len(Transaction.objects.filter(account__user=self.user)))

    def test_no_transactions(self):
        Transaction.objects.all().delete()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data),0)

    def test_transactions_from_one_account(self):
        self.url = reverse('transactions',kwargs={'account_id':'abc'})
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data),len(Transaction.objects.filter(account='abc')))

    def test_invalid_account(self):
        self.url = reverse('transactions',kwargs={'account_id':'invalid_id'})
        response = self.client.get(self.url)
        self.assertEquals(len(response.data),0)

    def test_user_cannot_see_transactions_in_other_users_account(self):
        self.user = User.objects.get(id=2) 
        self.client.force_authenticate(self.user)
        self.url = reverse('transactions',kwargs={'account_id':'abc'})
        response = self.client.get(self.url)
        self.assertEquals(len(response.data),0)

    
