import json

from django.test import TestCase, RequestFactory
from rest_framework.test import force_authenticate
from crypto_exchanges.serializers import *
from crypto_exchanges.views import *


class CryptoExchangeAccountViewTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', first_name='Lesya', last_name='Abakhova',
                                             email='example@hse.edu.ru', password='testpassword')

        self.crypto_exchange_account_binance = CryptoExchangeAccount.objects.create(
            user=self.user,
            crypto_exchange_name='Binance'
        )
        self.crypto_exchange_account_binance.save()

        self.crypto_exchange_account_gateio = CryptoExchangeAccount.objects.create(
            user=self.user,
            crypto_exchange_name='Gateio'
        )
        self.crypto_exchange_account_gateio.save()

        self.crypto_exchange_account_coinlist = CryptoExchangeAccount.objects.create(
            user=self.user,
            crypto_exchange_name='CoinList'
        )
        self.crypto_exchange_account_coinlist.save()

        self.crypto_exchange_account_coinbase = CryptoExchangeAccount.objects.create(
            user=self.user,
            crypto_exchange_name='CoinBase'
        )
        self.crypto_exchange_account_coinbase.save()

        self.crypto_exchange_account_kraken = CryptoExchangeAccount.objects.create(
            user=self.user,
            crypto_exchange_name='Kraken'
        )
        self.crypto_exchange_account_kraken.save()

    def test_delete_binance(self):
        url = '/crypto-exchanges/binance'

        request = self.factory.delete(url, data=json.dumps({'id': self.crypto_exchange_account_binance.id}),
                                      content_type='application/json')

        force_authenticate(request, user=self.user)

        view = BinanceView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(CryptoExchangeAccount.objects.filter(id=self.crypto_exchange_account_binance.id).exists())

    def test_delete_gateio(self):
        url = '/crypto-exchanges/gateio'

        request = self.factory.delete(url, data=json.dumps({'id': self.crypto_exchange_account_gateio.id}),
                                      content_type='application/json')

        force_authenticate(request, user=self.user)

        view = GateioView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(CryptoExchangeAccount.objects.filter(id=self.crypto_exchange_account_gateio.id).exists())

    def test_delete_coinlist(self):
        url = '/crypto-exchanges/coinlist'

        request = self.factory.delete(url, data=json.dumps({'id': self.crypto_exchange_account_coinlist.id}),
                                      content_type='application/json')

        force_authenticate(request, user=self.user)

        view = CoinListView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(CryptoExchangeAccount.objects.filter(id=self.crypto_exchange_account_coinlist.id).exists())

    def test_delete_coinbase(self):
        url = '/crypto-exchanges/coinbase'

        request = self.factory.delete(url, data=json.dumps({'id': self.crypto_exchange_account_coinbase.id}),
                                      content_type='application/json')

        force_authenticate(request, user=self.user)

        view = CoinBaseView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(CryptoExchangeAccount.objects.filter(id=self.crypto_exchange_account_coinbase.id).exists())

    def test_delete_kraken(self):
        url = '/crypto-exchanges/kraken'

        request = self.factory.delete(url, data=json.dumps({'id': self.crypto_exchange_account_kraken.id}),
                                      content_type='application/json')

        force_authenticate(request, user=self.user)

        view = KrakenView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(CryptoExchangeAccount.objects.filter(id=self.crypto_exchange_account_kraken.id).exists())

    def test_delete_binance_unauthorised(self):
        other_user = User.objects.create_user(username='otheruser', first_name='Lesya', last_name='Abakhova',
                                              email='la@hse.edu.ru')

        url = '/crypto_exchange_accounts/binance/'

        request = self.factory.delete(url, data=json.dumps({'id': self.crypto_exchange_account_binance.id}),
                                      content_type='application/json')

        force_authenticate(request, user=other_user)

        view = BinanceView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.assertTrue(CryptoExchangeAccount.objects.filter(id=self.crypto_exchange_account_binance.id).exists())

    def test_delete_gateio_unauthorised(self):
        other_user = User.objects.create_user(username='otheruser', first_name='Lesya', last_name='Abakhova',
                                              email='la@hse.edu.ru')

        url = '/crypto_exchange_accounts/gateio/'

        request = self.factory.delete(url, data=json.dumps({'id': self.crypto_exchange_account_gateio.id}),
                                      content_type='application/json')

        force_authenticate(request, user=other_user)

        view = GateioView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.assertTrue(CryptoExchangeAccount.objects.filter(id=self.crypto_exchange_account_binance.id).exists())

    def test_delete_coinlist_unauthorised(self):
        other_user = User.objects.create_user(username='otheruser', first_name='Lesya', last_name='Abakhova',
                                              email='la@hse.edu.ru')

        url = '/crypto_exchange_accounts/coinlist/'

        request = self.factory.delete(url, data=json.dumps({'id': self.crypto_exchange_account_coinlist.id}),
                                      content_type='application/json')

        force_authenticate(request, user=other_user)

        view = CoinListView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.assertTrue(CryptoExchangeAccount.objects.filter(id=self.crypto_exchange_account_coinlist.id).exists())

    def test_delete_coinbase_unauthorised(self):
        other_user = User.objects.create_user(username='otheruser', first_name='Lesya', last_name='Abakhova',
                                              email='la@hse.edu.ru')

        url = '/crypto_exchange_accounts/binance/'

        request = self.factory.delete(url, data=json.dumps({'id': self.crypto_exchange_account_coinbase.id}),
                                      content_type='application/json')

        force_authenticate(request, user=other_user)

        view = CoinBaseView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.assertTrue(CryptoExchangeAccount.objects.filter(id=self.crypto_exchange_account_coinbase.id).exists())

    def test_delete_kraken_unauthorised(self):
        other_user = User.objects.create_user(username='otheruser', first_name='Lesya', last_name='Abakhova',
                                              email='la@hse.edu.ru')

        url = '/crypto_exchange_accounts/binance/'

        request = self.factory.delete(url, data=json.dumps({'id': self.crypto_exchange_account_kraken.id}),
                                      content_type='application/json')

        force_authenticate(request, user=other_user)

        view = KrakenView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.assertTrue(CryptoExchangeAccount.objects.filter(id=self.crypto_exchange_account_kraken.id).exists())