from django.test import TestCase
from crypto_exchanges.services import *


class TestGenericExchangeFetcher(TestCase):
    def setUp(self):
        self.api_key = ""
        self.secret_key = ""
        self.fetcher = ExchangeFetcher(api_key=self.api_key, secret_key=self.secret_key)

    def test_get_current_time(self):

        current_time = self.fetcher.get_current_time()
        self.assertIsInstance(current_time, int)
        self.assertAlmostEquals(current_time, round(time.time() * 1000))

    def test_prehash(self):

        timestamp = str(int(time.time()))
        method = 'GET'
        path = '/v1/hello-world/'
        body = None
        prehash = self.fetcher.prehash(timestamp=timestamp, method=method, path=path, body=body)
        self.assertIsInstance(prehash, str)
        self.assertEquals(prehash, timestamp + method.upper() + path + (body or ''))

    def test_hash(self):

        timestamp = str(int(time.time()))
        hashed = self.fetcher.hash(timestamp=timestamp)
        self.assertIsInstance(hashed, str)
        self.assertEquals(hashed,
                          hmac.new(self.secret_key.encode('utf-8'), timestamp.encode('utf-8'), sha256).hexdigest())

    def test_signature(self):

        with self.assertRaises(NotImplementedError):
            self.fetcher.signature()

    def test_get_account_data(self):

        with self.assertRaises(NotImplementedError):
            self.fetcher.get_account_data()

    def test_get_trading_history(self):

        with self.assertRaises(NotImplementedError):
            self.fetcher.get_trading_history()

