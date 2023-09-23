from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from django.urls import reverse
from accounts.models import User
from banking.models import Account, Transaction
from rest_framework import status

class DeleteAccountViewTestCase(TestCase):
    
    fixtures = [
        'accounts/fixtures/user.json',
        'banking/tests/fixtures/bank_data.json'
    ]

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.get(id=1) 
        self.client.force_authenticate(self.user)

    def test_url(self):
        self.url = reverse('delete_account', kwargs={'account_id':'abc'})
        self.assertEqual(self.url,'/banking/delete_account/abc/')

    def test_delete_account(self):
        before = len(Account.objects.filter(user=self.user))
        self.url = reverse('delete_account', kwargs={'account_id':'abc'})
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        after = len(Account.objects.filter(user=self.user))
        self.assertEqual(response.data,{'Success': 'Deleted'})
        self.assertEqual(before-1,after)

    def test_delete_invalid_account(self):
        before = len(Account.objects.all())
        self.url = reverse('delete_account', kwargs={'account_id':'invalid_id'})
        self.client.get(self.url)
        after = len(Account.objects.all())
        self.assertEqual(before,after) # Should have the same number of accounts

    def test_user_cannot_delete_another_users_account(self):
        before = len(Account.objects.all())
        self.url = reverse('delete_account', kwargs={'account_id':'abc'})
        self.user = User.objects.get(id=2) 
        self.client.force_authenticate(self.user)
        self.client.get(self.url)
        after = len(Account.objects.all())
        self.assertEqual(before,after) # Should have the same number of accounts