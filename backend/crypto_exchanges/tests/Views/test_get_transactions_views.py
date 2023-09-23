from datetime import datetime
from typing import Any, Dict, List
import pytz
from rest_framework.test import force_authenticate
from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import User
from django.test import TestCase
from ...views import get_transactions
from crypto_exchanges.serializers import *
from collections import OrderedDict


def convert_to_dict_list(data: List[OrderedDict]) -> List[Dict[str, Any]]:
    result = []
    for item in data:
        dict_item = {}
        for key, value in item.items():
            dict_item[key] = value
        result.append(dict_item)
    return result


class TestGetTransactions(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username='@user', first_name='Name', last_name='Lastname',
                                             email='namelastname@example.org')
        self.crypto_exchange_account = CryptoExchangeAccount.objects.create(
            user=self.user,
            crypto_exchange_name='Binance',
            api_key='wfeioguhwe549876y43jh',
            secret_key='wfjbh234987trfhu'
        )

    def test_get_transactions(self):
        transaction = Transaction.objects.create(
            crypto_exchange_object=self.crypto_exchange_account,
            timestamp=datetime.now(pytz.timezone('Europe/London')),
            transaction_type="buy",
            amount=1.0,
            asset='BTC'
        )

        transaction.save()

        url = f'/crypto-exchanges/get_transactions/{self.crypto_exchange_account.id}/'
        request = self.factory.get(url)
        force_authenticate(request, user=self.user)
        response = get_transactions(request, self.crypto_exchange_account.id)
        self.assertEqual(response.status_code, 200)
        expected_data = [{'crypto_exchange_object': self.crypto_exchange_account.id, 'asset': 'BTC',
                          'transaction_type': 'buy', 'amount': 1.0,
                          'timestamp': str(transaction.timestamp.isoformat()).replace('+00:00', 'Z')
                          }]
        self.assertEqual(convert_to_dict_list(response.data), expected_data)

    def test_get_transactions_with_empty_data(self):
        url = f'/crypto-exchanges/get_transactions/{self.crypto_exchange_account.id}/'
        request = self.factory.get(url)
        force_authenticate(request, user=self.user)
        response = get_transactions(request, self.crypto_exchange_account.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, ['empty'])
