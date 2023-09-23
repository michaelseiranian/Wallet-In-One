from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from accounts.models import User
from rest_framework.exceptions import ErrorDetail
from stocks.models import Transaction

""" Tests for calculating Metrics for a User's stock accounts """
class MetricsViewTestCase(TestCase):
    fixtures = [
        'stocks/tests/fixtures/user.json',
        'stocks/tests/fixtures/stocks.json',
        'stocks/tests/fixtures/transaction.json'
    ]

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.get(id=3)  
        self.client.force_authenticate(self.user)
        self.url = reverse('get_stock_metrics')

    def test_url(self):
        self.assertEqual(self.url,'/stocks/get_metrics/')

    def test_successful_get_metrics(self):
        self.url = reverse('get_stock_metrics')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 5)
        self.assertEqual(len(response.data['all']), 11)
        self.assertEqual(response.data['all']['total_number_of_transactions'], 1)

    def test_unsuccessful_get_metrics(self):
        self.url = reverse('get_stock_metrics')
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.data['detail'],  ErrorDetail(string='Method "POST" not allowed.', code='method_not_allowed'))
        self.assertEqual(len(response.data), 1)

    def test_no_metrics(self):
        user = User.objects.get(id=1)
        self.client.force_authenticate(user)
        self.url = reverse('get_stock_metrics')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 5)
        self.assertEqual(len(response.data['all']), 11)
        self.assertEqual(response.data['all']['total_number_of_transactions'], 0)