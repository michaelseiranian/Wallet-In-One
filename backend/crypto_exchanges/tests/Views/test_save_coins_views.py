from django.contrib.auth.models import User
from django.test import TestCase
from unittest.mock import MagicMock
from ...views import BinanceView, GateioView, CoinListView, CoinBaseView, KrakenView
from crypto_exchanges.serializers import *


class SaveCoinsTestCase(TestCase):

    def test_binance_view_save_coins(self):
        binance = BinanceView()
        filtered_data = [{'asset': 'BTC', 'free': '1.0', 'locked': '0'}, {'asset': 'ETH', 'free': '0.5', 'locked': '0'}]
        request = MagicMock()
        new_user = User.objects.create_user(username='testuser', password='testpass')
        request.user = new_user
        saved_exchange_account_object = CryptoExchangeAccount.objects.create(user=new_user,
                                                                             crypto_exchange_name='Binance',
                                                                             api_key='apikey', secret_key='secretkey')
        binance.save_coins(filtered_data, request, saved_exchange_account_object)

        self.assertEqual(saved_exchange_account_object.token_set.count(), 2)
        self.assertEqual(saved_exchange_account_object.token_set.get(asset='BTC').free_amount, 1.0)
        self.assertEqual(saved_exchange_account_object.token_set.get(asset='ETH').free_amount, 0.5)

    def test_gateio_view_save_coins(self):
        gateio = GateioView()
        filtered_data = [{'currency': 'BTC', 'available': '1.0', 'locked': '0'},
                         {'currency': 'ETH', 'available': '0.5', 'locked': '0'}]
        request = MagicMock()
        new_user = User.objects.create_user(username='testuser', password='testpass')
        request.user = new_user
        saved_exchange_account_object = CryptoExchangeAccount.objects.create(user=new_user,
                                                                             crypto_exchange_name='Binance',
                                                                             api_key='apikey', secret_key='secretkey')
        gateio.save_coins(filtered_data, request, saved_exchange_account_object)

        self.assertEqual(saved_exchange_account_object.token_set.count(), 2)
        self.assertEqual(saved_exchange_account_object.token_set.get(asset='BTC').free_amount, 1.0)
        self.assertEqual(saved_exchange_account_object.token_set.get(asset='ETH').free_amount, 0.5)

    def test_coin_list_view_save_coins(self):
        coin_list = CoinListView()
        filtered_data = [('BTC', 1.0), ('ETH', 0.5)]
        request = MagicMock()
        new_user = User.objects.create_user(username='testuser', password='testpass')
        request.user = new_user
        saved_exchange_account_object = CryptoExchangeAccount.objects.create(user=new_user,
                                                                             crypto_exchange_name='Binance',
                                                                             api_key='apikey', secret_key='secretkey')
        coin_list.save_coins(filtered_data, request, saved_exchange_account_object)

        self.assertEqual(saved_exchange_account_object.token_set.count(), 2)
        self.assertEqual(saved_exchange_account_object.token_set.get(asset='BTC').free_amount, 1.0)
        self.assertEqual(saved_exchange_account_object.token_set.get(asset='ETH').free_amount, 0.5)

    def test_coin_base_view_save_coins(self):
        coin_base = CoinBaseView()
        filtered_data = [{'currency': 'BTC', 'amount': '1.0'}, {'currency': 'ETH', 'amount': '0.5'}]
        request = MagicMock()
        new_user = User.objects.create_user(username='testuser', password='testpass')
        request.user = new_user
        saved_exchange_account_object = CryptoExchangeAccount.objects.create(user=new_user,
                                                                             crypto_exchange_name='Binance',
                                                                             api_key='apikey', secret_key='secretkey')
        coin_base.save_coins(filtered_data, request, saved_exchange_account_object)

        self.assertEqual(saved_exchange_account_object.token_set.count(), 2)
        self.assertEqual(saved_exchange_account_object.token_set.get(asset='BTC').free_amount, 1.0)
        self.assertEqual(saved_exchange_account_object.token_set.get(asset='ETH').free_amount, 0.5)

    def test_kraken_view_save_coins(self):
        kraken = KrakenView()
        filtered_data = [('BTC', 1.0), ('ETH', 0.5)]
        request = MagicMock()
        new_user = User.objects.create_user(username='testuser', password='testpass')
        request.user = new_user
        saved_exchange_account_object = CryptoExchangeAccount.objects.create(user=new_user,
                                                                             crypto_exchange_name='Binance',
                                                                             api_key='apikey', secret_key='secretkey')
        kraken.save_coins(filtered_data, request, saved_exchange_account_object)

        self.assertEqual(saved_exchange_account_object.token_set.count(), 2)
        self.assertEqual(saved_exchange_account_object.token_set.get(asset='BTC').free_amount, 1.0)
        self.assertEqual(saved_exchange_account_object.token_set.get(asset='ETH').free_amount, 0.5)

