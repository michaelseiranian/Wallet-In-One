from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from accounts.models import User
from rest_framework.exceptions import ErrorDetail
from stocks.models import Transaction


""" Tests for a Accessing a specific transaction """
class GetTransactionViewTestCase(TestCase):
    fixtures = [
        'stocks/tests/fixtures/user.json',
        'stocks/tests/fixtures/stocks.json',
        'stocks/tests/fixtures/transaction.json'
    ]

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.get(id=3)  
        self.client.force_authenticate(self.user)
        self.url = reverse('getTransaction',kwargs={'id':'2'})

    def test_url(self):
        self.assertEqual(self.url,'/stocks/get_transaction/2/')

    def test_successful_get_transaction(self):
        self.url = reverse('getTransaction',kwargs={'id':'2'})
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], 2)

    def test_unsuccessful_get_transaction(self):
        self.url = reverse('getTransaction',kwargs={'id':'2'})
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.data['detail'],  ErrorDetail(string='Method "POST" not allowed.', code='method_not_allowed'))
        self.assertEqual(len(response.data), 1)
