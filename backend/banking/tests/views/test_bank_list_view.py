from django.test import TestCase, Client
from rest_framework.test import APIClient
from django.urls import reverse
from accounts.models import User
from rest_framework import status
from banking.services import get_institutions

class BankListViewTestCase(TestCase):
    
    fixtures = [
        'accounts/fixtures/user.json',
    ]

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.get(id=1)  
        self.client.force_authenticate(self.user)
        self.url = reverse('bank_list')

    def test_url(self):
        self.assertEqual(self.url,'/banking/bank_list/')

    def test_response(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, get_institutions())
    