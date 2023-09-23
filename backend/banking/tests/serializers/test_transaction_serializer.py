from django.test import TestCase
from accounts.models import User
from banking.models import Transaction
from banking.serializers import TransactionSerializer

class TransactionSerializerTest(TestCase):
    fixtures = [
        'accounts/fixtures/user.json',
        'banking/tests/fixtures/bank_data.json'
    ]

    def setUp(self):
        self.user = User.objects.get(id=1) 
        self.transaction = Transaction.objects.get(id=1)

    def test_transaction_serializer(self):
        serializer = TransactionSerializer(self.transaction)
        self.assertEqual(serializer.data['time'],'2022-12-01T13:41:31Z' )
        self.assertEqual(serializer.data['amount_currency'],'GBP' )
        self.assertEqual(serializer.data['amount'],'100.00' )
        self.assertEqual(serializer.data['info'],'Income' )
        self.assertEqual(serializer.data['account'],'abc' )
        self.assertEqual(serializer.data['formatted_amount'], {'string': '£100.00', 'currency': 'GBP', 'amount': '100.00'})