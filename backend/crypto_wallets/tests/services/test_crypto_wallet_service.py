from django.test import TestCase
from crypto_wallets.services import CryptoWalletService, get_timestamp, normalise_value


class CryptoWalletServiceTestCase(TestCase):

    def test_valid_crypto_wallet_request(self):
        crypto_wallets_service = CryptoWalletService('Bitcoin', '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa')
        self.assertIsInstance(crypto_wallets_service.type, str)
        self.assertIsInstance(crypto_wallets_service.balance, int)
        self.assertIsInstance(crypto_wallets_service.received, int)
        self.assertIsInstance(crypto_wallets_service.spent, int)
        self.assertIsInstance(crypto_wallets_service.output_count, int)
        self.assertIsInstance(crypto_wallets_service.unspent_output_count, int)
        self.assertIsInstance(crypto_wallets_service.transactions, list)

    def test_invalid_crypto_wallet_request(self):
        crypto_wallets_service = CryptoWalletService('Invalid', 'Invalid')
        self.assertIsNone(crypto_wallets_service.type)

    def test_get_timestamp(self):
        timestamp = get_timestamp("2023-01-01 14:32:54")
        self.assertEqual(timestamp, 1672583574)

    def test_invalid_get_timestamp(self):
        self.assertRaises(ValueError, get_timestamp, "???")

    def test_normalise_value(self):
        self.assertEqual(normalise_value('Bitcoin', 75634545), 0.75634545)
        self.assertEqual(normalise_value('Bitcoin-Cash', 342), 0.00000342)
        self.assertEqual(normalise_value('Litecoin', 8), 0.00000008)
        self.assertEqual(normalise_value('Dogecoin', 97565), 0.00097565)
        self.assertEqual(normalise_value('Dash', 5922), 0.00005922)
        self.assertEqual(normalise_value('Groestlcoin', 4003), 0.00004003)
        self.assertEqual(normalise_value('Zcash', 67400), 0.000674)
        self.assertEqual(normalise_value('eCash', 23545), 235.45)

    def test_unknown_normalise_value(self):
        value = 100
        self.assertEqual(normalise_value('Unknown', value), value)

