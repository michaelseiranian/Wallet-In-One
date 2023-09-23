from django.test import TestCase
from banking.services import *
from banking.models import Transaction
from unittest.mock import patch
from django.utils import timezone
from banking.tests.helpers import disable_updates
from unittest.mock import Mock, patch

class ServiceRouteTestCase(TestCase):
    # Can't use real accounts because it would contains personal information
    # These tests are just making sure these helper functions are able to call the api.

    fixtures = [
        'accounts/fixtures/user.json',
        'banking/tests/fixtures/bank_data.json'
    ]

    def setUp(self):
        self.transaction_data = {'transactions': {'booked':[
            {
                "bookingDate": "2022-12-20",
                "valueDate": "2022-12-20",
                "bookingDateTime": "2022-12-20T12:20:19Z",
                "valueDateTime": "2022-12-20T00: 00: 00.000Z",
                "transactionAmount": {
                    "amount": "5.00",
                    "currency": "GBP"
                },
                "remittanceInformationUnstructured": "Test 1",
                "internalTransactionId": "123"
            },
            {
                "bookingDate": "2022-12-20",
                "valueDate": "2022-12-20",
                "bookingDateTime": "2022-12-20T12:20:19Z",
                "valueDateTime": "2022-12-20T00: 00: 00.000Z",
                "transactionAmount": {
                    "amount": "-10.00",
                    "currency": "GBP"
                },
                "remittanceInformationUnstructuredArray": ["Test 2"],
                "internalTransactionId": "1234"
            },
            {
                "bookingDate": "2022-12-20",
                "valueDate": "2022-12-20",
                "bookingDateTime": "2022-12-20T12:20:19Z",
                "valueDateTime": "2022-12-20T00: 00: 00.000Z",
                "transactionAmount": {
                    "amount": "5.00",
                    "currency": "GBP"
                },
                "remittanceInformationUnstructuredArray": ["Test 4"],
                "internalTransactionId": "12345"
            }
        ]}}

        self.balance_data = {"balances":[
            {
                "balanceAmount": {
                    "amount": "500.67",
                    "currency": "GBP"
                },
                "balanceType": "expected",
                "referenceDate": "2023-11-19"
            }
        ]}

        self.disbled_transaction_data = {'transactions': {'booked':[
            {
                'error': 'account_disabled'
            },
        ]}}

        self.disabled_balance_data = {"balances":[
            {
                'error': 'account_disabled'
            }
        ]}

    def test_get_account_data_calls_api(self):
        self.assertEquals(get_account_data('1'),{'summary': 'Not found.', 'detail': 'Not found.', 'status_code': 404})

    def test_get_account_balances_calls_api(self):
        self.assertEquals(get_account_balances('1'),{'summary': 'Invalid Account ID', 'detail': '1 is not a valid Account UUID. ', 'status_code': 400})

    def test_get_account_transactions_calls_api(self):
        self.assertEquals(get_account_transactions('1'),{'summary': 'Invalid Account ID', 'detail': '1 is not a valid Account UUID. ', 'status_code': 400})

    def test_get_account_details_calls_api(self):
        self.assertEquals(get_account_details('1'),{'summary': 'Invalid Account ID', 'detail': '1 is not a valid Account UUID. ', 'status_code': 400})

    def test_get_institution_calls_api(self):
        self.assertEquals(get_institution('bank'),{'summary': 'Not found.', 'detail': 'Not found.', 'status_code': 404})

    def test_get_requisitions_calls_api(self):
        self.assertEquals(get_requisitions('1'),{'summary': 'Not found.', 'detail': 'Not found.', 'status_code': 404})

    def test_total_user_balance(self):
        disable_updates()
        # Test balance is returned for a user with a bank account
        self.assertEqual(str(total_user_balance(User.objects.get(id=1))),'£100.00')
        
        # Test balance is 0 for a user without any bank accounts
        self.assertEqual(str(total_user_balance(User.objects.get(id=3))),'£0.00')

    @patch('requests.get')
    def test_update_account_transactions(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200

        mock_response.json = lambda: self.transaction_data

        mock_get.return_value = mock_response
    
        before_count = Transaction.objects.all().count()
        update_account_transactions(Account.objects.all().first())
        after_count = Transaction.objects.all().count()
        self.assertEqual(before_count+3, after_count) # 3 new transactions should have been added


    @patch('requests.get')
    def test_update_account_balance(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200

        mock_response.json = lambda: self.balance_data
        mock_get.return_value = mock_response
    
        self.assertEqual(str(Account.objects.all().first().account_balance()),'£100.00')
        update_account_balance(Account.objects.all().first())
        self.assertEqual(str(Account.objects.all().first().account_balance()),'£500.67') # Account balance should update

    @patch('requests.get')
    def test_update_user_accounts(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200

        def mock_json():
            url = mock_get.call_args[0][0]
            if 'transactions' in url:
                return self.transaction_data
            if 'balances' in url:
                return self.balance_data
        mock_response.json = mock_json
        mock_get.return_value = mock_response

        self.user = User.objects.all().first()
        self.accounts = Account.objects.filter(user=self.user) 

        before_count = Transaction.objects.all().count()
        self.assertEqual(str(Account.objects.all().first().account_balance()),'£100.00')
        update_user_accounts(self.user)
        after_count = Transaction.objects.all().count()
        self.assertEqual(before_count+3, after_count) 
        self.assertEqual(str(Account.objects.all().first().account_balance()),'£500.67')


    @patch('requests.get')
    def test_update_user_accounts_when_an_account_is_disabled(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200

        def mock_json():
            url = mock_get.call_args[0][0]
            if 'transactions' in url:
                return self.disbled_transaction_data
            if 'balances' in url:
                return self.disabled_balance_data
            if 'abc' in url:
                return {'status': "SUSPENDED"}
            if 'def' in url:
                return {'status': "INACTIVE"}

        mock_response.json = mock_json
        mock_get.return_value = mock_response

        self.user = User.objects.all().first()
        self.accounts = Account.objects.filter(user=self.user) 

        before_count = Transaction.objects.all().count()
        self.assertEqual(str(Account.objects.all().first().account_balance()),'£100.00')
        self.assertEqual(Account.objects.get(id='abc').disabled,False)
        self.assertEqual(Account.objects.get(id='def').disabled,False)

        update_user_accounts(self.user)

        after_count = Transaction.objects.all().count()
        self.assertEqual(before_count, after_count)  # No transactions should have been added
        self.assertEqual(str(Account.objects.all().first().account_balance()),'£100.00') # Balance should not have changed
        
        self.assertEqual(Account.objects.get(id='abc').disabled,True) # Account should now be updated to disabled
        self.assertEqual(Account.objects.get(id='def').disabled,False) 

        
        
