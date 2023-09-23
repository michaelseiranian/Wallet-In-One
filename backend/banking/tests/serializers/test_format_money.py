from django.test import TestCase
from banking.serializers import format_money
from djmoney.money import Money

class FormatMoneyTestCase(TestCase):
    def setUp(self):
        self.money = Money(100,'GBP')
        self.money2 = Money(-100,'GBP')
    
    def test_positive(self):
        result = format_money(self.money)
        self.assertEqual(result['string'],'£100.00')
        self.assertEqual(result['currency'],'GBP')
        self.assertEqual(result['amount'],'100')
        
    def test_negative(self):
        result = format_money(self.money2)
        self.assertEqual(result['string'],'-£100.00')
        self.assertEqual(result['currency'],'GBP')
        self.assertEqual(result['amount'],'-100')


