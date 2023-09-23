from django.core.exceptions import ValidationError
from django.test import TestCase
from accounts.models import User
from banking.models import Account, Balance, Transaction
from djmoney.money import Money
from django.utils import timezone


class AccountModelTestCase(TestCase):
    """Unit tests for the account model."""

    fixtures = [
        'accounts/fixtures/user.json',
        'banking/tests/fixtures/bank_data.json'
    ]

    def setUp(self):
        self.user = User.objects.get(id=1)
        self.account = Account.objects.get(id='abc')
        self.account.last_update = timezone.now()
        self.account.save()

    def test_account_valid(self):
        self._assert_is_valid()

    def test_id_cannot_be_none(self):
        self.account.id = None
        self._assert_is_invalid()

    def test_id_cannot_be_larger_than_1024(self):
        self.account.id = '1'*1025
        self._assert_is_invalid()

    def test_id_can_be_1024(self):
        self.account.id = '1'*1024
        self._assert_is_valid()

    def test_can_update(self):
        self.assertFalse(self.account.can_update())
        time = timezone.now()
        self.account.last_update = None
        self.assertTrue(self.account.can_update())
        self.assertGreaterEqual(self.account.last_update,time)

    def test_add_transactions(self):
        test_data = [
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
                "internalTransactionId": "123"
            }
        ]
        before = len(Transaction.objects.all())
        self.account.add_transactions(test_data)
        after = len(Transaction.objects.all())

        self.assertEqual(before+2, after)

    def test_add_balances(self):
        test_data = [
            {
                "balanceAmount": {
                    "amount": "657.49",
                    "currency": "GBP"
                },
                "balanceType": "expected",
                "referenceDate": "2021-11-22"
            },
            {
                "balanceAmount": {
                    "amount": "185.67",
                    "currency": "GBP"
                },
                "balanceType": "expected",
                "referenceDate": "2021-11-19"
            }
        ]

        Balance.objects.all().delete()
        self.assertEqual(len(Balance.objects.all()),0)
        self.account.add_balances(test_data)
        self.assertEqual(len(Balance.objects.all()),2)

    def test_add_balance_if_balance_already_exists(self):
        self.balance = Balance.objects.get(id=1)
        self.assertEqual(len(Balance.objects.all()),4)
        self.assertEqual(self.account.account_balance(),Money(100,'GBP'))

        test_data = [
            {
                "balanceAmount": {
                    "amount": "300.00",
                    "currency": "GBP"
                },
                "balanceType": "expected",
                "referenceDate": "2022-11-01" # same date
            },
        ]
        self.account.add_balances(test_data)

        self.assertEqual(len(Balance.objects.all()),4)
        self.assertEqual(self.account.account_balance(),Money(300,'GBP'))

    def test_account_balance(self):
        self.assertEqual(self.account.account_balance(),Money(100,'GBP'))
        Balance.objects.all().delete()
        self.assertEqual(self.account.account_balance(),Money(0,'GBP'))

    def _assert_is_valid(self):
        try:
            self.account.full_clean()
        except (ValidationError):
            self.fail('Test account should be valid')

    def _assert_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.account.full_clean()