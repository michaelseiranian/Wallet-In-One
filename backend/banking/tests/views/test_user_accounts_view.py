from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from django.urls import reverse
from accounts.models import User
from banking.models import Account, Transaction
from rest_framework import status

class UserAccountsViewTestCase(TestCase):
    
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
        self.url = reverse('user_accounts')

    def test_url(self):
        self.assertEqual(self.url,'/banking/user_accounts/')

    def test_response_from_all_accounts_from_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(Account.objects.filter(user=self.user)))
        response_account = response.data[0]
        database_account = Account.objects.filter(user=self.user).first()

        self.assertEqual(response_account['id'],database_account.id)
        self.assertEqual(response_account['requisition_id'],str(database_account.requisition_id))
        self.assertEqual(response_account['iban'],database_account.iban)
        self.assertEqual(response_account['institution_id'],database_account.institution_id)
        self.assertEqual(response_account['institution_name'],database_account.institution_name)
        self.assertEqual(response_account['institution_logo'],database_account.institution_logo)
        self.assertEqual(response_account['color'],database_account.color)
        self.assertEqual(response_account['disabled'],database_account.disabled)
        self.assertEqual(response_account['user'],database_account.user.id)
        self.assertIn("balance",response_account )

    def test_user_with_no_accounts(self):
        self.user = User.objects.get(id=2) 
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data),0)

    def test_no_accounts_all_deleted(self):
        Account.objects.all().delete()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data),0)

    def test_one_account(self):
        self.url = reverse('user_accounts',kwargs={'account_id':'abc'})
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data),1)
        self.assertEquals(response.data[0]['id'],'abc')

    def test_invalid_account(self):
        self.url = reverse('user_accounts',kwargs={'account_id':'invalid_id'})
        response = self.client.get(self.url)
        self.assertEquals(len(response.data),0)

    def test_user_cannot_see_other_users_account(self):
        self.user = User.objects.get(id=2) 
        self.client.force_authenticate(self.user)
        self.url = reverse('user_accounts',kwargs={'account_id':'abc'})
        response = self.client.get(self.url)
        self.assertEquals(len(response.data),0)

    
