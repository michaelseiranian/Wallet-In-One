from django.test import TestCase
from accounts.models import User
from stocks.models import Transaction
import plaid
from djmoney.money import Money
from stocks.services import calculate_metrics, chart_breakdown_stocks, total_stock_balance, setUpClient, PLAID_CLIENT_ID, PLAID_SECRET
from decimal import Decimal

""" Unit Tests for Stocks Services """
class ServicesTest(TestCase):
    fixtures = [
        'stocks/tests/fixtures/user.json',
        'stocks/tests/fixtures/stocks.json',
        'stocks/tests/fixtures/transaction.json'
    ]

    def setUp(self):
        self.user = User.objects.get(id=3)
        self.transactions = Transaction.objects.all()

    def test_metrics(self):
        metrics = calculate_metrics(self.transactions)
        self.assertEqual(metrics['total_number_of_transactions'], 1)
        self.assertEqual(metrics['highest_transaction'], 2307.21)
        self.assertEqual(metrics['lowest_transaction'], 2307.21)
        self.assertEqual(metrics['average_transaction'], 2307.21)
        self.assertEqual(metrics['variance'], 0)
        self.assertEqual(metrics['standard_deviation'], 0)
        self.assertEqual(metrics['highest_fee'], 0.5)
        self.assertEqual(metrics['lowest_fee'], 0.5)
        self.assertEqual(metrics['average_fee'], 0.5)
        self.assertEqual(metrics['average_latitude'], 35.5)
        self.assertEqual(metrics['average_longitude'], 37.0)

    def test_chart_breakdown(self):
        chart_breakdown = (chart_breakdown_stocks(self.user))[0]
        self.assertEqual(chart_breakdown['x'], 'Test Stock Account-Test Institution')
        self.assertEqual(chart_breakdown['y'], Decimal('100.00'))
        self.assertEqual(chart_breakdown['id'], '1')

    def test_total_stock_balance(self):
        self.assertEqual(total_stock_balance(self.user), Money('100.00', 'GBP'))

    def test_total_stock_balance_no_accounts(self):
        user = User.objects.get(id=1)
        self.assertEqual(total_stock_balance(user), 0)

    def test_set_up_client(self):
        client = setUpClient()
        self.assertEqual(client.api_client.configuration.host, plaid.Environment.Sandbox)
        self.assertEqual(client.api_client.configuration.api_key['clientId'], PLAID_CLIENT_ID)
        self.assertEqual(client.api_client.configuration.api_key['secret'], PLAID_SECRET)
        self.assertEqual(client.api_client.configuration.api_key['plaidVersion'], '2020-09-14')