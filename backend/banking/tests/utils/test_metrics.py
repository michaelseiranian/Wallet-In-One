from django.test import TestCase
from django.utils import timezone
from accounts.models import User
from banking.util import calculate_metrics_all, calculate_metrics, calculate_balance_history, bar_data,group_transactions
from banking.models import Account, Transaction
from decimal import Decimal
from djmoney.money import Money
class MetricsTestCase(TestCase):
    
    fixtures = [
        'accounts/fixtures/user.json',
        'banking/tests/fixtures/bank_data.json'
    ]

    def setUp(self):
        self.user = User.objects.get(id=1)
        self.transactions = Transaction.objects.all()
        self.balance = self.transactions[0].account.account_balance()
    
    def test_metrics(self):
        fixture = {'positive': {'total_amount_of_transactions': 4, 'highest_transaction': Decimal('200'), 'lowest_transaction': Decimal('100'), 'average_transaction': Decimal('125'), 'variance': Decimal('1875'), 'standard_deviation': Decimal('43.3012701892219'), 'bar_data': {'labels': ['December', 'January', 'February'], 'values': [Decimal('100.00'), Decimal('300.00'), Decimal('100.00')], 'data': {'2023-02-01': Decimal('100.00'), '2023-01-01': Decimal('300.00'), '2022-12-01': Decimal('100.00')}}, 'net': Decimal('500')}, 'negative': {'total_amount_of_transactions': 3, 'highest_transaction': Decimal('-50'), 'lowest_transaction': Decimal('-50'), 'average_transaction': Decimal('-50'), 'variance': 0, 'standard_deviation': 0, 'bar_data': {'labels': ['December', 'January', 'February'], 'values': [Decimal('-50.00'), Decimal('-50.00'), Decimal('-50.00')], 'data': {'2023-02-01': Decimal('-50.00'), '2023-01-01': Decimal('-50.00'), '2022-12-01': Decimal('-50.00')}}, 'net': Decimal('-150')}, 'both': {'total_amount_of_transactions': 7, 'highest_transaction': Decimal('200'), 'lowest_transaction': Decimal('-50'), 'average_transaction': Decimal('50'), 'variance': Decimal('8571.42857142857'), 'standard_deviation': Decimal('92.5820099772551'), 'bar_data': {'labels': ['December', 'January', 'February'], 'values': [Decimal('50.00'), Decimal('250.00'), Decimal('50.00')], 'data': {'2023-02-01': Decimal('50.00'), '2023-01-01': Decimal('250.00'), '2022-12-01': Decimal('50.00')}}, 'net': Decimal('350')}, 'balance_history': {'2023-02-15': Decimal('100.00'), '2023-02-01': Decimal('150.00'), '2023-01-15': Decimal('50.00'), '2023-01-01': Decimal('100.00'), '2022-12-15': Decimal('-200.00'), '2022-12-01': Decimal('-150.00')}, 'highest_balance': Decimal('150.00'), 'lowest_balance': Decimal('-200.00'), 'total_money_in': Decimal('500'), 'total_money_out': Decimal('-150'), 'net': Decimal('350')}
        result = calculate_metrics_all(self.transactions, self.balance)
        self.assertEqual(fixture,result)

    def test_balance_history(self):
        fixture =  {'2023-02-15': '£100.00', '2023-02-01': '£150.00', '2023-01-15': '£50.00', '2023-01-01': '£100.00', '2022-12-15': '-£200.00', '2022-12-01': '-£150.00'}
        result = calculate_balance_history(self.transactions, self.balance, interval='day', format=True)
        self.assertEqual(fixture,result)
        result = calculate_balance_history(self.transactions, self.balance, interval='time', format=True)
        fixture = {'2023-02-15 13:41:31+00:00': '£100.00', '2023-02-01 13:41:31+00:00': '£150.00', '2023-01-15 13:41:31+00:00': '£50.00', '2023-01-01 13:41:31+00:00': '£100.00', '2022-12-15 13:41:31+00:00': '-£200.00', '2022-12-01 13:41:31+00:00': '-£150.00'}
        self.assertEqual(fixture,result)
        result = calculate_balance_history(self.transactions, self.balance, interval='month', format=True)
        fixture = {'2023-02-01': '£100.00', '2023-01-01': '£50.00', '2022-12-01': '-£200.00'}
        self.assertEqual(fixture,result)

    def test_bar_data(self):
        result = bar_data(self.transactions,'month')
        fixture = {'labels': ['December', 'January', 'February'], 'values': [Decimal('50.00'), Decimal('250.00'), Decimal('50.00')], 'data': {'2023-02-01': Decimal('50.00'), '2023-01-01': Decimal('250.00'), '2022-12-01': Decimal('50.00')}}
        self.assertEqual(fixture,result)
        result = bar_data(self.transactions,'day')
        fixture = {'labels': ['01', '15', '01', '15', '01', '15'], 'values': [Decimal('100.00'), Decimal('-50.00'), Decimal('300.00'), Decimal('-50.00'), Decimal('100.00'), Decimal('-50.00')], 'data': {'2023-02-15': Decimal('-50.00'), '2023-02-01': Decimal('100.00'), '2023-01-15': Decimal('-50.00'), '2023-01-01': Decimal('300.00'), '2022-12-15': Decimal('-50.00'), '2022-12-01': Decimal('100.00')}}
        self.assertEqual(fixture,result)

    def test_group_transactions(self):
        result = group_transactions(self.transactions, interval="day")
        fixture = {'2023-02-15': Money('-50.00', 'GBP'), '2023-02-01': Money('100.00', 'GBP'), '2023-01-15': Money('-50.00', 'GBP'), '2023-01-01': Money('300.00', 'GBP'), '2022-12-15': Money('-50.00', 'GBP'), '2022-12-01': Money('100.00', 'GBP')}
        self.assertEqual(fixture,result)
        result = group_transactions(self.transactions, interval="month")
        fixture = {'2023-02-01': Money('50.00', 'GBP'), '2023-01-01': Money('250.00', 'GBP'), '2022-12-01': Money('50.00', 'GBP')}
        self.assertEqual(fixture,result)
        with self.assertRaises(UnboundLocalError):
            group_transactions(self.transactions, interval="invalid")



