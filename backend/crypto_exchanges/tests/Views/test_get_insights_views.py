from unittest.mock import patch
from rest_framework.test import APIRequestFactory, force_authenticate
from accounts.models import User
from django.test import TestCase
from crypto_exchanges.views import get_insights


class GetInsightsTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        self.user = User.objects.create_user(username='@user', first_name='Name', last_name='Lastname',
                                             email='namelastname@example.org')

    @patch('crypto_exchanges.views.get_all_transactions')
    @patch('crypto_exchanges.views.get_most_expensive_transaction')
    def test_get_insights_success(self, mock_most_expensive_transaction, mock_all_transactions):
        mock_all_transactions.return_value = ['transaction1', 'transaction2']
        mock_most_expensive_transaction.return_value = ('BTC', 1.0, 10000.0, 'buy', '2022-01-01 00:00:00+00:00', 'exchange1')
        request = self.factory.get('crypto-exchanges/get_insights/')

        force_authenticate(request, user=self.user)
        response = get_insights(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {
            'all_transactions': ['transaction1', 'transaction2'],
            'most_expensive_transaction': ('BTC', 1.0, 10000.0, 'buy', '2022-01-01 00:00:00+00:00', 'exchange1')
        })

    @patch('crypto_exchanges.views.get_all_transactions')
    @patch('crypto_exchanges.views.get_most_expensive_transaction')
    def test_get_insights_empty(self, mock_most_expensive_transaction, mock_all_transactions):
        mock_all_transactions.return_value = ['empty']
        mock_most_expensive_transaction.return_value = ('empty', 0.0, 0.0, None, None, None)
        request = self.factory.get('crypto-exchanges/get_insights/')

        force_authenticate(request, user=self.user)
        response = get_insights(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {
            'all_transactions': ['empty'],
            'most_expensive_transaction': ('empty', 0.0, 0.0, None, None, None)
        })
