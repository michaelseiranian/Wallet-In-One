from abc import ABC, ABCMeta, abstractmethod
from datetime import datetime
import pytz

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from crypto_exchanges.serializers import TransactionSerializer, CryptoExchangeAccountSerializer
from crypto_exchanges.services import CurrentMarketPriceFetcher, get_all_transactions, get_most_expensive_transaction, \
    BinanceFetcher, CoinBaseFetcher, CoinListFetcher, KrakenFetcher, GateioFetcher
from crypto_exchanges.models import Transaction, CryptoExchangeAccount, Token


# Data time translation
def millis_to_datetime(millis):
    return datetime.fromtimestamp(millis / 1000.0)


# Data time translation
def iso8601_to_datetime(iso8601_string):
    dt = datetime.strptime(iso8601_string, '%Y-%m-%dT%H:%M:%S.%fZ')
    return dt


# Data time translation
def unix_timestamp_to_datetime(unix_timestamp):
    dt = datetime.fromtimestamp(unix_timestamp)
    return dt


# Views
# Crypto exchange insights - The most expensive transaction
@api_view(['GET'])
def get_insights(request):
    all_transactions = get_all_transactions(request)
    most_expensive_transaction = get_most_expensive_transaction(request)
    insights = {'all_transactions': all_transactions, 'most_expensive_transaction': most_expensive_transaction}
    return Response(insights)


@api_view(['GET'])
def get_transactions(request, exchange):
    exchange_obj = CryptoExchangeAccount.objects.get(id=exchange)
    transactions = Transaction.objects.filter(crypto_exchange_object=exchange_obj).order_by('timestamp')
    data = TransactionSerializer(transactions, many=True).data
    if len(data) == 0:
        data.append('empty')
    return Response(data)


@api_view(['GET'])
def get_token_breakdown(request, exchange):
    exchange_obj = CryptoExchangeAccount.objects.get(id=exchange)
    crypto_data_from_exchanges = CurrentMarketPriceFetcher(request.user).get_exchange_token_breakdown(exchange_obj)
    if len(crypto_data_from_exchanges['token_data']) == 0:
        crypto_data_from_exchanges['token_data'] = [{'x': 'empty'}]
    return Response(crypto_data_from_exchanges)


@api_view(['GET'])
def get_exchange_balances(request):
    return Response(CurrentMarketPriceFetcher(request.user).chart_breakdown_crypto_exchanges())


# Generic class for crypto exchanges
class GenericCryptoExchanges(APIView):
    __metaclass__ = ABCMeta

    def __init__(self, crypto_exchange_name=None, fetcher=None, **kwargs):
        super().__init__(**kwargs)
        self.account_ids = None
        self.crypto_exchange_name = crypto_exchange_name
        self.fetcher = fetcher

    # Function to check for errors in the API call
    @abstractmethod
    def check_for_errors_from_the_response_to_the_api_call(self, data, service):
        if self.fetcher == BinanceFetcher:
            if 'msg' in data:
                # encountering an error while retrieving data
                return Response({'error': data['msg']}, status=status.HTTP_400_BAD_REQUEST)
        elif self.fetcher == GateioFetcher:
            if 'label' and 'message' in data:
                # encountering an error while retrieving data
                return Response({'error': data['message']}, status=status.HTTP_400_BAD_REQUEST)
        elif self.fetcher == CoinListFetcher:
            if 'status' in data and (data['status'] != 'ok' or data['status'] != '200'):
                # encountering an error while retrieving data
                return Response({'error': data['message']}, status=status.HTTP_400_BAD_REQUEST)
        elif self.fetcher == CoinBaseFetcher:
            if 'errors' in data:
                # encountering an error while retrieving data
                return Response({'error': data['errors'][0]['message']}, status=status.HTTP_400_BAD_REQUEST)
        elif self.fetcher == KrakenFetcher:
            if 'error' in data and 'result' not in data:
                # encountering an error while retrieving data
                return Response({'error': data['error'][0]}, status=status.HTTP_400_BAD_REQUEST)

    # Abstract inner function for filtering data
    @abstractmethod
    def filter_not_empty_balance(self, coin_to_check):
        pass

    # Abstract function for passing data in the right format
    @abstractmethod
    def get_data_unified(self, data):
        pass

    # Abstract method for saving coin objects to the database
    @abstractmethod
    def save_coins(self, filtered_data, request, saved_exchange_account_object):
        pass

    # Abstract method for saving transaction objects to the database
    @abstractmethod
    def save_transactions(self, transactions, request, saved_exchange_account_object):
        pass

    # Abstract get call
    @abstractmethod
    def get(self, request):
        crypto_exchange_accounts = CryptoExchangeAccount.objects.filter(user=request.user)
        account_serializers = CryptoExchangeAccountSerializer(crypto_exchange_accounts, many=True)
        serializer_array = account_serializers.data
        for serializer in serializer_array:
            exchange = CryptoExchangeAccount.objects.get(user=request.user, api_key=serializer['api_key'])
            serializer.update({'id': exchange.id})
        return Response(serializer_array)

    # Abstract post call
    @abstractmethod
    def post(self, request):
        # CryptoExchangeAccount.objects.get(crypto_exchange_name="CoinList").delete()
        # Pass the data to the serialiser so that the binance account can be created
        # Create a field 'crypto_exchange' in the request dict to prevent double adding the same account
        request.data['crypto_exchange_name'] = self.crypto_exchange_name

        # Create an account
        account = CryptoExchangeAccountSerializer(data=request.data, context={'request': request})

        # Validate data
        account.is_valid(raise_exception=True)

        # Checking if the account has already been registered
        if bool(CryptoExchangeAccount.objects.filter(user=request.user,
                                                     crypto_exchange_name=request.data['crypto_exchange_name'],
                                                     api_key=request.data['api_key'],
                                                     secret_key=request.data['secret_key'])):
            return Response({'error': f'This account from {self.crypto_exchange_name} has already been added'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Use the provided API key and secret key to connect to the Binance API
        service = self.fetcher(request.data['api_key'], request.data['secret_key'])

        # Get the user's account information
        data = service.get_account_data()

        # Making sure the api and secret keys are valid before saving the account
        checker: Response = self.check_for_errors_from_the_response_to_the_api_call(data, service)
        if checker:
            return checker

        # Save the binance account to the database
        saved_exchange_account_object = account.save()
        filtered_data = list(filter(self.filter_not_empty_balance, self.get_data_unified(data)))
        self.save_coins(filtered_data, request, saved_exchange_account_object)
        transactions = service.get_trading_history()
        self.save_transactions(transactions, request, saved_exchange_account_object)
        return Response(filtered_data, status=status.HTTP_200_OK)

    # Abstract delete call
    def delete(self, request):
        crypto_exchange_account = CryptoExchangeAccount.objects.get(id=request.data['id'])
        if crypto_exchange_account.user != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = CryptoExchangeAccountSerializer(crypto_exchange_account)
        crypto_exchange_account.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Binance
class BinanceView(GenericCryptoExchanges, ABC):
    def __init__(self):
        super().__init__('Binance', BinanceFetcher)

    # Inner function for filtering data
    def filter_not_empty_balance(self, coin_to_check):
        super(BinanceView, self).filter_not_empty_balance(coin_to_check)
        return float(coin_to_check['free']) > 0

    def get_data_unified(self, data):
        super(BinanceView, self).get_data_unified(data)
        return data['balances']

    def save_coins(self, filtered_data, request, saved_exchange_account_object):
        super(BinanceView, self).save_coins(filtered_data, request, saved_exchange_account_object)
        for coin in filtered_data:
            # Add token info
            token = Token()
            token.user = request.user
            token.asset = coin['asset']
            token.crypto_exchange_object = saved_exchange_account_object
            token.free_amount = float(coin['free'])
            token.locked_amount = float(coin['locked'])
            token.save()

    def save_transactions(self, transactions, request, saved_exchange_account_object):
        super(BinanceView, self).save_transactions(transactions, request, saved_exchange_account_object)
        for symbol in transactions.values():
            for binance_transaction in symbol:
                transaction = Transaction()
                transaction.crypto_exchange_object = saved_exchange_account_object
                transaction.asset = binance_transaction['symbol']
                if binance_transaction['isBuyer']:
                    transaction.transaction_type = 'buy'
                else:
                    transaction.transaction_type = 'sell'
                transaction.amount = binance_transaction['qty']

                naive_datetime = millis_to_datetime(binance_transaction['time'])
                utc_timezone = pytz.timezone('UTC')
                aware_datetime = utc_timezone.localize(naive_datetime)
                transaction.timestamp = aware_datetime

                transaction.save()

    def get(self, request):
        return super(BinanceView, self).get(request)

    def post(self, request):
        return super(BinanceView, self).post(request)

    def delete(self, request):
        return super(BinanceView, self).delete(request)


# GateIo
class GateioView(GenericCryptoExchanges, ABC):
    def __init__(self):
        super().__init__('GateIo', GateioFetcher)

    # Inner function for filtering data
    def filter_not_empty_balance(self, coin_to_check):
        super(GateioView, self).filter_not_empty_balance(coin_to_check)
        return float(coin_to_check['available']) > 0

    def get_data_unified(self, data):
        super(GateioView, self).get_data_unified(data)
        return data

    def save_coins(self, filtered_data, request, saved_exchange_account_object):
        super(GateioView, self).save_coins(filtered_data, request, saved_exchange_account_object)
        for coin in filtered_data:
            # check if the coin already exists
            token = Token()
            token.user = request.user
            token.crypto_exchange_object = saved_exchange_account_object
            token.asset = coin['currency']
            token.free_amount = float(coin['available'])
            token.locked_amount = float(coin['locked'])
            token.save()

    def save_transactions(self, transactions, request, saved_exchange_account_object):
        super(GateioView, self).save_transactions(transactions, request, saved_exchange_account_object)
        for symbol in transactions.values():
            for gateio_transaction in symbol:
                transaction = Transaction()
                transaction.crypto_exchange_object = saved_exchange_account_object
                transaction.asset = gateio_transaction['currency_pair']
                transaction.transaction_type = gateio_transaction['side']
                transaction.amount = gateio_transaction['amount']

                # Avoid naive data time warning
                naive_datetime = millis_to_datetime(float(gateio_transaction['create_time_ms']))
                utc_timezone = pytz.timezone('UTC')
                aware_datetime = utc_timezone.localize(naive_datetime)
                transaction.timestamp = aware_datetime

                transaction.save()

    def get(self, request):
        return super(GateioView, self).get(request)

    def post(self, request):
        return super(GateioView, self).post(request)

    def delete(self, request):
        return super(GateioView, self).delete(request)


# CoinList
class CoinListView(GenericCryptoExchanges, ABC):
    def __init__(self):
        super().__init__('CoinList', CoinListFetcher)

    # Inner function for filtering data
    def filter_not_empty_balance(self, coin_to_check):
        super(CoinListView, self).filter_not_empty_balance(coin_to_check)
        return float(coin_to_check[1]) > 0

    def get_data_unified(self, data):
        super(CoinListView, self).get_data_unified(data)
        return data['asset_balances'].items()

    def save_coins(self, filtered_data, request, saved_exchange_account_object):
        super(CoinListView, self).save_coins(filtered_data, request, saved_exchange_account_object)
        for coin in filtered_data:
            # check if the coin already exists
            token = Token()
            token.user = request.user
            token.crypto_exchange_object = saved_exchange_account_object
            token.asset = coin[0]
            token.free_amount = float(coin[1])
            token.locked_amount = float(0)
            token.save()

    def save_transactions(self, transactions, request, saved_exchange_account_object):
        super(CoinListView, self).save_transactions(transactions, request, saved_exchange_account_object)
        for symbol in transactions.values():
            for coinlist_transaction in symbol:
                transaction = Transaction()
                transaction.crypto_exchange_object = saved_exchange_account_object
                if coinlist_transaction['symbol'] is None:
                    transaction.asset = coinlist_transaction['asset']
                else:
                    transaction.asset = coinlist_transaction['symbol']

                if coinlist_transaction['transaction_type'] == "XFER":
                    transaction.transaction_type = "sell"
                elif coinlist_transaction['transaction_type'] == "SWAP":
                    transaction.transaction_type = "buy"
                else:
                    transaction.transaction_type = coinlist_transaction['transaction_type']

                if coinlist_transaction['amount'] == '':
                    transaction.amount = 0
                elif float(coinlist_transaction['amount']) < 0:
                    transaction.amount = float(coinlist_transaction['amount']) * -1
                else:
                    transaction.amount = float(coinlist_transaction['amount'])

                # Avoid naive data time warning
                naive_datetime = iso8601_to_datetime(coinlist_transaction['created_at'])
                utc_timezone = pytz.timezone('UTC')
                aware_datetime = utc_timezone.localize(naive_datetime)
                transaction.timestamp = aware_datetime

                transaction.save()

    def get(self, request):
        return super(CoinListView, self).get(request)

    def post(self, request):
        return super(CoinListView, self).post(request)

    def delete(self, request):
        return super(CoinListView, self).delete(request)


# CoinBase
class CoinBaseView(GenericCryptoExchanges, ABC):
    def __init__(self):
        super().__init__('CoinBase', CoinBaseFetcher)

    def filter_not_empty_balance(self, coin_to_check):
        super(CoinBaseView, self).filter_not_empty_balance(coin_to_check)
        return float(coin_to_check['amount']) > 0

    def get_data_unified(self, data):
        super(CoinBaseView, self).get_data_unified(data)
        return data

    def save_coins(self, filtered_data, request, saved_exchange_account_object):
        super(CoinBaseView, self).save_coins(filtered_data, request, saved_exchange_account_object)
        for coin in filtered_data:
            # check if the coin already exists
            token = Token()
            token.user = request.user
            token.crypto_exchange_object = saved_exchange_account_object
            token.asset = coin['currency']
            token.free_amount = float(coin['amount'])
            token.locked_amount = float(0)
            token.save()

    def save_transactions(self, transactions, request, saved_exchange_account_object):
        super(CoinBaseView, self).save_transactions(transactions, request, saved_exchange_account_object)
        transactions_fills = transactions.get('fills')
        for coinbase_transaction in transactions_fills:
            transaction = Transaction()
            transaction.crypto_exchange_object = saved_exchange_account_object
            transaction.asset = coinbase_transaction['product_id']

            if coinbase_transaction['trade_type'] == 'FILL':
                transaction.transaction_type = 'buy'
            elif coinbase_transaction['trade_type'] == 'REVERSAL':
                transaction.transaction_type = 'sell'
            else:
                transaction.transaction_type = coinbase_transaction['trade_type']

            transaction.amount = coinbase_transaction['size']

            # Avoid naive data time warning
            naive_datetime = iso8601_to_datetime(coinbase_transaction['trade_time'])
            utc_timezone = pytz.timezone('UTC')
            aware_datetime = utc_timezone.localize(naive_datetime)
            transaction.timestamp = aware_datetime

            transaction.save()

    def get(self, request):
        return super(CoinBaseView, self).get(request)

    def post(self, request):
        return super(CoinBaseView, self).post(request)

    def delete(self, request):
        return super(CoinBaseView, self).delete(request)


# Kraken
class KrakenView(GenericCryptoExchanges, ABC):
    def __init__(self):
        super().__init__('Kraken', KrakenFetcher)

    def filter_not_empty_balance(self, coin_to_check):
        super(KrakenView, self).filter_not_empty_balance(coin_to_check)
        return float(coin_to_check[1]) > 0

    def get_data_unified(self, data):
        super(KrakenView, self).get_data_unified(data)
        return data['result'].items()

    def save_coins(self, filtered_data, request, saved_exchange_account_object):
        super(KrakenView, self).save_coins(filtered_data, request, saved_exchange_account_object)
        for coin in filtered_data:
            # check if the coin already exists
            token = Token()
            token.user = request.user
            token.crypto_exchange_object = saved_exchange_account_object
            token.asset = coin[0]
            token.free_amount = float(coin[1])
            token.locked_amount = float(0)
            token.save()

    def save_transactions(self, transactions, request, saved_exchange_account_object):
        super(KrakenView, self).save_transactions(transactions, request, saved_exchange_account_object)
        transactions = transactions['result']['trades']
        for kraken_transaction in transactions:
            transaction = Transaction()
            transaction.crypto_exchange_object = saved_exchange_account_object
            transaction.asset = kraken_transaction['pair']

            if kraken_transaction['type'] == 'all':
                transaction.transaction_type = 'buy'
            elif kraken_transaction['type'] == 'closed position':
                transaction.transaction_type = 'sell'
            else:
                transaction.transaction_type = kraken_transaction['type']

            transaction.amount = kraken_transaction['vol']

            # Avoid naive data time warning
            naive_datetime = unix_timestamp_to_datetime(kraken_transaction['time'])
            utc_timezone = pytz.timezone('UTC')
            aware_datetime = utc_timezone.localize(naive_datetime)
            transaction.timestamp = aware_datetime

            transaction.save()

    def get(self, request):
        return super(KrakenView, self).get(request)

    def post(self, request):
        return super(KrakenView, self).post(request)

    def delete(self, request):
        return super(KrakenView, self).delete(request)


# Update the existing tokens retrieved from crypto exchanges
class UpdateAllTokens(APIView):
    def post(self, request):
        fixed_accounts = CryptoExchangeAccount.objects.filter(user=request.user)
        for account in fixed_accounts:
            api_key = account.api_key
            secret_key = account.secret_key
            platform = account.crypto_exchange_name
            account.delete()
            request.data['api_key'] = api_key
            request.data['secret_key'] = secret_key
            response = 0
            if platform == 'Binance':
                response = BinanceView()
            elif platform == 'GateIo':
                response = GateioView()
            elif platform == 'CoinList':
                response = CoinListView()
            elif platform == 'CoinBase':
                response = CoinBaseView()
            elif platform == 'Kraken':
                response = KrakenView()
            else:
                pass
            response.post(request)
        return Response({'message': 'Success. Data was updated successfully'}, status=status.HTTP_200_OK)
