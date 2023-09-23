import requests
import time
import hmac
from hashlib import sha256, sha512
from base64 import b64encode, b64decode
from datetime import datetime, timezone
from urllib.parse import quote_plus, urlencode
from crypto_exchanges.serializers import TransactionSerializer
from crypto_exchanges.models import Token, CryptoExchangeAccount, Transaction
from abc import ABC, ABCMeta, abstractmethod
from collections import defaultdict
from urllib.parse import urlencode

from crypto_exchanges.models import Token, CryptoExchangeAccount

from abc import abstractmethod

# Data time translation
def iso8601_to_datetime(iso8601_string):
    dt = datetime.strptime(iso8601_string, '%Y-%m-%d %H:%M:%S.%f%z')
    return dt

# Generic fetcher class
class ExchangeFetcher:
    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key

    # Timestamp
    def get_current_time(self):
        return round(time.time() * 1000)

    # Prehashing that is required for some further hashing
    def prehash(self, timestamp, method, path, body):
        return timestamp + method.upper() + path + (body or '')

    # Hashing that is required for signature validation
    def hash(self, timestamp):
        return hmac.new(self.secret_key.encode('utf-8'), timestamp.encode('utf-8'), sha256).hexdigest()

    # Abstract signature creation
    @abstractmethod
    def signature(self, *args, **kwargs):
        raise NotImplementedError("Subclasses must implement this method")

    # Abstract account data retrieval
    @abstractmethod
    def get_account_data(self):
        raise NotImplementedError("Subclasses must implement this method")

    # Abstract trading history retrieval
    @abstractmethod
    def get_trading_history(self):
        raise NotImplementedError("Subclasses must implement this method")


# Class was implemented according to: "https://binance-docs.github.io/apidocs/spot/en/#change-log"
class BinanceFetcher(ExchangeFetcher):
    def __init__(self, api_key, secret_key):
        super().__init__(api_key, secret_key)
        self.symbols = ['BTCUSDT', 'ETHUSDT', 'ADAUSDT', 'XRPUSDT', 'SOLUSDT']

    def signature(self, params):
        query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
        return hmac.new(self.secret_key.encode('utf-8'), query_string.encode('utf-8'), sha256).hexdigest()

    def get_account_data(self, timestamp=None):
        endpoint = "https://api.binance.com/api"
        # Timestamp may be passed for testing to avoid CPU racing (e.g. concurrency racing)
        if not timestamp:
            timestamp = f"timestamp={self.get_current_time()}"
        request_url = f"{endpoint}/v3/account?{timestamp}&signature={self.hash(timestamp)}"
        # Set headers
        headers = {'X-MBX-APIKEY': self.api_key}
        response = requests.get(url=request_url, headers=headers)
        return response.json()

    def get_trading_history(self, timestamp=None):
        to_return = {}
        for symbol in self.symbols:
            # Timestamp may be passed for testing to avoid CPU racing (e.g. concurrency racing)
            if not timestamp:
                timestamp = str(self.get_current_time())
            params = {'symbol': symbol, 'timestamp': timestamp}
            signature = self.signature(params)
            request_url = "https://api.binance.com/api/v3/myTrades"
            # Set headers
            headers = {'X-MBX-APIKEY': self.api_key}
            response = requests.get(request_url, headers=headers, params={**params, **{'signature': signature}})
            # Filtering data
            to_return[symbol] = response.json()

        return to_return


# Class was implemented according to: "https://www.gate.io/docs/developers/apiv4/en/"
class GateioFetcher(ExchangeFetcher):
    def __init__(self, api_key, secret_key):
        super().__init__(api_key, secret_key)
        self.symbols = ['BTC_USDT', 'ETH_USDT', 'ADA_USDT', 'XRP_USDT', 'SOL_USDT', 'ARV_USDT']
        self.host = 'https://api.gateio.ws'
        self.prefix = '/api/v4'
        self.headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

    def signature(self, method, url, query_string=None, payload_string=None, timestamp=None):
        # Timestamp may be passed for testing to avoid CPU racing (e.g. concurrency racing)
        if not timestamp:
            timestamp = str(time.time())
        message = sha512()
        message.update((payload_string or "").encode('utf-8'))
        hashed_payload = message.hexdigest()
        path = '%s\n%s\n%s\n%s\n%s' % (method, url, query_string or "", hashed_payload, timestamp)
        signature = hmac.new(self.secret_key.encode('utf-8'), path.encode('utf-8'), sha512).hexdigest()
        return {'KEY': self.api_key, 'Timestamp': timestamp, 'SIGN': signature}

    def get_account_data(self):
        endpoint = f"{self.host}{self.prefix}/spot/accounts"
        query_param = ''
        sign_headers = self.signature('GET', self.prefix + '/spot/accounts', query_param)
        # Set headers
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        headers.update(sign_headers)
        response = requests.get(endpoint, headers=headers)
        return response.json()

    def get_trading_history(self):
        # Limit response time
        limit = 10
        to_return = {}
        for currency_pair in self.symbols:
            url = f"/spot/trades?currency_pair={currency_pair}&limit={limit}"
            sign_headers = self.signature('GET', self.prefix + url)
            # Set headers
            headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
            headers.update(sign_headers)
            response = requests.get(self.host + self.prefix + url, headers=headers)
            # Filtering data
            to_return[currency_pair] = response.json()
        return to_return


# Class was implemented according to: "https://coinlist.co/help/api"
class CoinListFetcher(ExchangeFetcher):

    def __init__(self, api_key, secret_key):
        super().__init__(api_key, secret_key)

    def signature(self, data, key):
        hmc = hmac.new(key, data.encode('utf-8'), digestmod=sha256)
        return b64encode(hmc.digest()).decode('utf-8')

    def get_account_data(self):
        endpoint = 'https://trade-api.coinlist.co'
        path = '/v1/accounts/'
        timestamp = str(int(time.time()))
        request_url = f"{endpoint}{path}"
        body = None
        method = 'GET'

        prehashed = self.prehash(timestamp, method, path, body)
        secret = b64decode(self.secret_key)
        signature = self.signature(prehashed, secret)

        # Set headers
        headers = {
            'Content-Type': 'application/json',
            'CL-ACCESS-KEY': self.api_key,
            'CL-ACCESS-SIG': signature,
            'CL-ACCESS-TIMESTAMP': timestamp
        }

        # Get response IDs
        response_id = requests.get(url=request_url, headers=headers)

        # Check for errors in the API response
        if 'accounts' not in response_id.json():
            return response_id.json()

        # We retrieved ID addresses of sub-accounts, its time to retrieve the actual data
        to_return = {}
        for account_id in response_id.json()['accounts']:
            endpoint = 'https://trade-api.coinlist.co'
            path = f"""/v1/accounts/{account_id['trader_id']}"""
            timestamp = str(int(time.time()))
            request_url = f"{endpoint}{path}"
            body = None
            method = 'GET'

            prehashed = self.prehash(timestamp, method, path, body)
            secret = b64decode(self.secret_key)
            signature = self.signature(prehashed, secret)

            # Set headers
            headers = {
                'Content-Type': 'application/json',
                'CL-ACCESS-KEY': self.api_key,
                'CL-ACCESS-SIG': signature,
                'CL-ACCESS-TIMESTAMP': timestamp
            }

            response = requests.get(url=request_url, headers=headers)
            # Filtering data
            to_return.update(response.json())

        return to_return

    def get_trading_history(self):
        endpoint = 'https://trade-api.coinlist.co'
        path = '/v1/accounts/'
        timestamp = str(int(time.time()))
        request_url = f"{endpoint}{path}"
        body = None
        method = 'GET'

        prehashed = self.prehash(timestamp, method, path, body)
        secret = b64decode(self.secret_key)
        signature = self.signature(prehashed, secret)

        # Set headers
        headers = {
            'Content-Type': 'application/json',
            'CL-ACCESS-KEY': self.api_key,
            'CL-ACCESS-SIG': signature,
            'CL-ACCESS-TIMESTAMP': timestamp
        }

        # Get response IDs
        response_id = requests.get(url=request_url, headers=headers)

        # Check for errors in the API response
        if 'accounts' not in response_id.json():
            return response_id.json()

        # We retrieved ID addresses of sub-accounts, its time to retrieve the actual data
        to_return = {}
        for account_id in response_id.json()['accounts']:
            endpoint = 'https://trade-api.coinlist.co'
            # path = f"""/v1/accounts/{account_id['trader_id']}"""
            path = f"/v1/accounts/{account_id['trader_id']}/ledger"
            timestamp = str(int(time.time()))
            request_url = f"{endpoint}{path}"
            body = None
            method = 'GET'

            prehashed = self.prehash(timestamp, method, path, body)
            secret = b64decode(self.secret_key)
            signature = self.signature(prehashed, secret)

            # Set headers
            headers = {
                'Content-Type': 'application/json',
                'CL-ACCESS-KEY': self.api_key,
                'CL-ACCESS-SIG': signature,
                'CL-ACCESS-TIMESTAMP': timestamp
            }

            response = requests.get(url=request_url, headers=headers)
            # Filtering data
            to_return.update(response.json())

        return to_return


# Class was implemented according to: "https://docs.cloud.coinbase.com/exchange/docs/requests"
# Create custom authentication for Coinbase API
class CoinBaseFetcher(ExchangeFetcher):
    def __init__(self, api_key, secret_key):
        super().__init__(api_key, secret_key)
        self.secret_key = secret_key.encode('utf-8')
        self.timestamp = str(int(time.time()))

    # Auth Base authorisation method
    def __call__(self, request):
        message = self.timestamp + request.method + request.path_url + (request.body or '')
        signature = self.signature(message)
        # Set headers
        request.headers.update({
            'CB-ACCESS-SIGN': signature,
            'CB-ACCESS-TIMESTAMP': self.timestamp,
            'CB-ACCESS-KEY': self.api_key,
        })
        return request

    def signature(self, message):
        return hmac.new(self.secret_key, message.encode(), sha256).hexdigest()

    def get_account_data(self):
        api_url = 'https://api.coinbase.com/v2/'
        # call the __call__ auth function
        auth = self

        response = requests.get(api_url + 'accounts', auth=auth)

        # Check for errors
        if response.status_code == 400 or response.status_code == 401 or response.status_code == 402 \
                or response.status_code == 403 or response.status_code == 404 or response.status_code == 405:
            return response.json()

        data_to_return = []

        # Filtering data
        data = response.json()['data']
        for coin in data:
            data_to_return.append(coin['balance'])

        return data_to_return

    def get_trading_history(self):
        auth = self
        api_url = "https://api.coinbase.com/api/v3/brokerage/orders/historical/fills"

        response = requests.get(api_url, auth=auth)

        return response.json()


# Class was implemented according to: "https://docs.kraken.com/rest/"
class KrakenFetcher(ExchangeFetcher):
    def __init__(self, api_key, secret_key):
        super().__init__(api_key, secret_key)

    # This method of getting the signature was taken from the API documentation and slightly modified
    def signature(self, urlpath, data, secret):
        post_data = urlencode(data)
        encoded = (str(data['nonce']) + post_data).encode()
        message = urlpath.encode() + sha256(encoded).digest()
        mac = hmac.new(b64decode(secret), message, sha512)
        sig_digest = b64encode(mac.digest())
        return sig_digest.decode()

    # Attaches auth headers and returns results of a POST request
    def get_account_data(self):
        # Construct the request and print the result
        url = 'https://api.kraken.com'
        path = '/0/private/Balance'
        timestamp = {"nonce": str(int(1000 * time.time()))}

        # Set headers
        headers = {
            'API-Key': self.api_key,
            'API-Sign': self.signature(path, timestamp, self.secret_key),
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.post((url + path), headers=headers, data=timestamp)

        return response.json()

    def get_trading_history(self):
        url = 'https://api.kraken.com'
        path = '/0/private/TradesHistory'
        timestamp = {"nonce": str(int(1000 * time.time()))}

        # Set headers
        headers = {
            'API-Key': self.api_key,
            'API-Sign': self.signature(path, timestamp, self.secret_key),
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.post((url + path), headers=headers, data=timestamp)

        return response.json()


# Test feature, code written by Krishna and modified by Ezzat, Michael
class CurrentMarketPriceFetcher:
    def __init__(self, user):
        self.user = user

    def get_crypto_price(self, symbol):
        url = f'https://min-api.cryptocompare.com/data/price?fsym={symbol}&tsyms=GBP'
        r = requests.get(url=url)
        response = r.json()
        try:
            price = float(response['GBP'])
        except KeyError:
            price = 0.0
        return price

    def total_user_balance_crypto(self):
        exchanges = CryptoExchangeAccount.objects.filter(user=self.user)
        total_balance = 0
        for exchange in exchanges:
            tokens = Token.objects.filter(crypto_exchange_object=exchange)
            total_balance += sum(
                self.get_crypto_price(token.asset) * (token.free_amount + token.locked_amount) for token in tokens)
        return round(total_balance, 2)

    def chart_breakdown_crypto_free(self):
        exchanges = CryptoExchangeAccount.objects.filter(user=self.user)
        if exchanges.exists():
            tokens = Token.objects.filter(crypto_exchange_object__in=exchanges)
            return [{'x': token.asset, 'y': round(self.get_crypto_price(token.asset) * token.free_amount, 2)}
                    for token in tokens]

    def chart_breakdown_crypto_locked(self):
        exchanges = CryptoExchangeAccount.objects.filter(user=self.user)
        if exchanges.exists():
            tokens = Token.objects.filter(crypto_exchange_object__in=exchanges)
            return [{'x': token.asset, 'y': round(self.get_crypto_price(token.asset) * token.locked_amount, 2)}
                    for token in tokens]

    def get_exchange_balance(self, exchange):
        tokens = Token.objects.filter(crypto_exchange_object=exchange)
        balance = 0
        for token in tokens:
            balance += self.get_crypto_price(token.asset) * (token.free_amount + token.locked_amount)
        return round(balance, 2)

    def get_exchange_token_breakdown(self, exchange):
        tokens = Token.objects.filter(crypto_exchange_object=exchange)
        dict_result = {}
        token_data = []
        balance = 0
        for token in tokens:
            price = self.get_crypto_price(token.asset)
            value = price * (token.free_amount + token.locked_amount)
            token_data.append({'x': token.asset + ": £" + str(round(value, 2)), 'y': round(value, 2)})
            balance += value
        dict_result.update({"balance": round(balance, 2), "token_data": sorted(token_data, key=lambda val: val['y'])})
        return dict_result

    def chart_breakdown_crypto_exchanges(self):
        exchanges = CryptoExchangeAccount.objects.filter(user=self.user)
        if exchanges.exists():
            return [{'x': exchange.crypto_exchange_name,
                     'y': self.get_exchange_balance(exchange), 'id': exchange.id}
                    for exchange in exchanges]


def get_all_transactions(request):
    transactions = Transaction.objects.filter(crypto_exchange_object__user=request.user).order_by('timestamp')
    data = TransactionSerializer(transactions, many=True).data
    if len(data) == 0:
        data = ['empty']
    return data


def get_most_expensive_transaction(request):
    transactions = Transaction.objects.filter(crypto_exchange_object__user=request.user)
    # Create dict with the highest amount of each asset for minimum API calls to crypto price fetcher
    asset_max_transactions = defaultdict(
        lambda: {'amount': 0.0, 'type': None, 'timestamp': None, 'exchange_name': None})
    for transaction in transactions:
        asset = transaction.asset[:3].upper()
        amount = transaction.amount
        if amount > asset_max_transactions[asset]['amount']:
            asset_max_transactions[asset]['amount'] = amount
            asset_max_transactions[asset]['type'] = transaction.transaction_type
            asset_max_transactions[asset]['timestamp'] = transaction.timestamp
            asset_max_transactions[asset]['exchange_name'] = transaction.crypto_exchange_object.crypto_exchange_name

    price_getter_obj = CurrentMarketPriceFetcher(request.user)
    most_expensive_transaction = None
    max_crypto_price_amount = 0.0
    # Look for the most expensive transaction
    for asset, data in asset_max_transactions.items():
        amount = data['amount']
        crypto_price = price_getter_obj.get_crypto_price(asset)  # Get price of crypto asset
        crypto_price_amount = crypto_price * amount
        if crypto_price_amount > max_crypto_price_amount:
            most_expensive_transaction = (
                asset, amount, round(crypto_price_amount, 2), data['type'], iso8601_to_datetime(str(data['timestamp'])).strftime('%Y-%m-%d %H:%M:%S'), data['exchange_name'])
            max_crypto_price_amount = crypto_price_amount

    if most_expensive_transaction is None:
        most_expensive_transaction = ('empty', 0.0, 0.0, None, None, None)
    return most_expensive_transaction
