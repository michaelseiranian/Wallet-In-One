from datetime import datetime, timedelta

from django.test import TestCase

from accounts.models import User
from crypto_wallets.models import CryptoWallet, CryptoWalletTransaction
from crypto_wallets.services import calculate_predicted_balance, calculate_received_spent, calculate_average_spend


class CryptoWalletInsightsTestCase(TestCase):

    fixtures = [
        'accounts/fixtures/user.json',
    ]

    def setUp(self):
        super(TestCase, self).setUp()
        self.user = User.objects.get(id=1)
        self.crypto_wallet = CryptoWallet(
            user=self.user,
            cryptocurrency="Bitcoin",
            symbol="BTC",
            address="0x0",
            balance=100.00,
            received=300.00,
            spent=200.00,
            output_count=50,
            unspent_output_count=20,
        )
        self.crypto_wallet.save()
        self.__setUpTransactions()

    def __setUpTransactions(self):
        self.crypto_wallet_transaction = CryptoWalletTransaction(
            crypto_wallet=self.crypto_wallet,
            value=10,
            time=(datetime.now() - timedelta(days=90)).timestamp(),
        )
        self.crypto_wallet_transaction.save()
        self.crypto_wallet_transaction = CryptoWalletTransaction(
            crypto_wallet=self.crypto_wallet,
            value=-10,
            time=datetime.now().timestamp(),
        )
        self.crypto_wallet_transaction.save()
        self.crypto_wallet_transaction = CryptoWalletTransaction(
            crypto_wallet=self.crypto_wallet,
            value=-20,
            time=datetime.now().timestamp(),
        )
        self.crypto_wallet_transaction.save()

    def test_calculate_predicted_balance(self):
        crypto_wallet_two = CryptoWallet(
            user=self.user,
            cryptocurrency="Bitcoin",
            symbol="ETH",
            address="0x1",
            balance=30.00,
            received=30.20,
            spent=10.30,
            output_count=50,
            unspent_output_count=20
        )
        crypto_wallet_two.save()
        self.crypto_wallet_transaction = CryptoWalletTransaction(
            crypto_wallet=crypto_wallet_two,
            value=-50,
            time=datetime.now().timestamp(),
        )
        self.crypto_wallet_transaction.save()

        crypto_wallet_three = CryptoWallet(
            user=self.user,
            cryptocurrency="Bitcoin",
            symbol="ETH",
            address="0x2",
            balance=0.00,
            received=30.20,
            spent=10.30,
            output_count=50,
            unspent_output_count=20
        )
        crypto_wallet_three.save()

        predicted_balance = calculate_predicted_balance(self.user)
        self.assertEqual(predicted_balance['BTC'], 70.0)
        self.assertEqual(predicted_balance['ETH'], -20.0)

    def test_calculate_predicted_balance_when_empty(self):
        CryptoWallet.objects.all().delete()
        predicted_balance = calculate_predicted_balance(self.user)
        self.assertEqual(predicted_balance, {})

    def test_calculate_predicted_balance_with_multiple_users(self):
        other_user = User.objects.get(id=2)
        crypto_wallet_two = CryptoWallet(
            user=other_user,
            cryptocurrency="Bitcoin",
            symbol="BTC",
            address="0x1",
            balance=200.00,
            received=30.20,
            spent=10.30,
            output_count=50,
            unspent_output_count=20
        )
        crypto_wallet_two.save()
        self.crypto_wallet_transaction = CryptoWalletTransaction(
            crypto_wallet=crypto_wallet_two,
            value=-50,
            time=datetime.now().timestamp(),
        )
        self.crypto_wallet_transaction.save()

        predicted_balance_one = calculate_predicted_balance(self.user)
        predicted_balance_two = calculate_predicted_balance(other_user)
        self.assertEqual(predicted_balance_one['BTC'], 70.0)
        self.assertEqual(predicted_balance_two['BTC'], 150.0)

    def test_calculate_received_spent(self):
        crypto_wallet_two = CryptoWallet(
            user=self.user,
            cryptocurrency="Bitcoin",
            symbol="BTC",
            address="0x1",
            balance=100.00,
            received=30.20,
            spent=10.30,
            output_count=50,
            unspent_output_count=20
        )
        crypto_wallet_two.save()

        crypto_wallet_three = CryptoWallet(
            user=self.user,
            cryptocurrency="Bitcoin",
            symbol="ETH",
            address="0x2",
            balance=100.00,
            received=50.00,
            spent=30.00,
            output_count=50,
            unspent_output_count=20
        )
        crypto_wallet_three.save()

        received_spent = calculate_received_spent(self.user)
        self.assertEqual(received_spent['BTC']['spent'], 210.3)
        self.assertEqual(received_spent['BTC']['received'], 330.2)
        self.assertEqual(received_spent['ETH']['spent'], 30.0)
        self.assertEqual(received_spent['ETH']['received'], 50.0)

    def test_calculate_received_spent_when_empty(self):
        CryptoWallet.objects.all().delete()
        received_spent = calculate_received_spent(self.user)
        self.assertEqual(received_spent, {})

    def test_calculate_received_spent_with_multiple_users(self):
        other_user = User.objects.get(id=2)
        crypto_wallet_two = CryptoWallet(
            user=other_user,
            cryptocurrency="Bitcoin",
            symbol="BTC",
            address="0x1",
            balance=100.00,
            received=30.20,
            spent=10.30,
            output_count=50,
            unspent_output_count=20
        )
        crypto_wallet_two.save()

        received_spent_one = calculate_received_spent(self.user)
        received_spent_two = calculate_received_spent(other_user)
        self.assertEqual(received_spent_one['BTC']['spent'], 200.0)
        self.assertEqual(received_spent_one['BTC']['received'], 300.0)
        self.assertEqual(received_spent_two['BTC']['spent'], 10.3)
        self.assertEqual(received_spent_two['BTC']['received'], 30.2)

    def test_calculate_average_spend(self):
        crypto_wallet_two = CryptoWallet(
            user=self.user,
            cryptocurrency="Bitcoin",
            symbol="ETH",
            address="0x1",
            balance=100.00,
            received=30.20,
            spent=10.30,
            output_count=50,
            unspent_output_count=20
        )
        crypto_wallet_two.save()
        self.crypto_wallet_transaction = CryptoWalletTransaction(
            crypto_wallet=crypto_wallet_two,
            value=-50,
            time=0,
        )
        self.crypto_wallet_transaction.save()

        average_spend = calculate_average_spend(self.user)
        self.assertEqual(average_spend['BTC'], -15.0)
        self.assertEqual(average_spend['ETH'], -50.0)

    def test_calculate_average_spend_when_empty(self):
        CryptoWallet.objects.all().delete()
        average_spend = calculate_average_spend(self.user)
        self.assertEqual(average_spend, {})

    def test_calculate_average_spend_with_multiple_users(self):
        other_user = User.objects.get(id=2)
        crypto_wallet_two = CryptoWallet(
            user=other_user,
            cryptocurrency="Bitcoin",
            symbol="BTC",
            address="0x1",
            balance=100.00,
            received=30.20,
            spent=10.30,
            output_count=50,
            unspent_output_count=20
        )
        crypto_wallet_two.save()
        self.crypto_wallet_transaction = CryptoWalletTransaction(
            crypto_wallet=crypto_wallet_two,
            value=-50,
            time=0,
        )
        self.crypto_wallet_transaction.save()

        average_spend_one = calculate_average_spend(self.user)
        average_spend_two = calculate_average_spend(other_user)
        self.assertEqual(average_spend_one['BTC'], -15.0)
        self.assertEqual(average_spend_two['BTC'], -50.0)
