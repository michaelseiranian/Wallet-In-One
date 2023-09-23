from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from accounts.models import User
from crypto_wallets.models import CryptoWallet


class CryptoWalletViewSetTestCase(TestCase):

    fixtures = [
        'accounts/fixtures/user.json',
    ]

    def setUp(self):
        super(TestCase, self).setUp()
        self.client = APIClient()
        self.user = User.objects.get(id=1)
        self.client.force_authenticate(self.user)

        self.url = reverse('api-root')
        self.list_url = reverse('crypto_wallet_view_set-list')
        self.detail_pk = 1
        self.detail_url = reverse('crypto_wallet_view_set-detail', kwargs={"pk": self.detail_pk})

        self.crypto_wallet = CryptoWallet(
            pk=1,
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
        self.crypto_wallet = CryptoWallet(
            user=self.user,
            cryptocurrency="Bitcoin",
            symbol="BTC",
            address="0x1",
            balance=100.00,
            received=300.00,
            spent=200.00,
            output_count=50,
            unspent_output_count=20,
        )
        self.crypto_wallet.save()

    def test_root_url(self):
        self.assertEqual(self.url, '/crypto_wallets/')

    def test_crypto_wallet_list_url(self):
        self.assertEqual(self.list_url, '/crypto_wallets/')

    def test_crypto_wallet_detail_url(self):
        self.assertEqual(self.detail_url, f'/crypto_wallets/{self.detail_pk}/')

    def test_unauthorised(self):
        self.client.logout()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    """Test Create"""

    def test_valid_create(self):
        wallet_count_before = CryptoWallet.objects.count()
        form_input = {'cryptocurrency': 'Bitcoin', 'symbol': 'BTC', 'address': '1P5ZEDWTKTFGxQjZphgWPQUpe554WKDfHQ'}
        response = self.client.post(self.list_url, form_input)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        wallet_count_after = CryptoWallet.objects.count()
        self.assertEqual(wallet_count_after, wallet_count_before + 1)
        created_wallet = CryptoWallet.objects.last()
        self.assertEqual(created_wallet.user, self.user)

        self.assertContains(response, 'cryptocurrency', status_code=201)
        self.assertContains(response, 'symbol', status_code=201)
        self.assertContains(response, 'address', status_code=201)
        self.assertContains(response, 'balance', status_code=201)
        self.assertContains(response, 'received', status_code=201)
        self.assertContains(response, 'spent', status_code=201)
        self.assertContains(response, 'output_count', status_code=201)
        self.assertContains(response, 'unspent_output_count', status_code=201)

    def test_create_with_bad_request(self):
        wallet_count_before = CryptoWallet.objects.count()
        form_input = {'cryptocurrency': 'Bitcoin', 'symbol': 'BTC', 'address': '???'}
        response = self.client.post(self.list_url, form_input)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        wallet_count_after = CryptoWallet.objects.count()
        self.assertEqual(wallet_count_after, wallet_count_before)

    """Test List"""
    def test_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, '0x0')
        self.assertContains(response, '0x1')

    def test_list_with_multiple_users(self):
        other_user = User.objects.get(id=2)
        self.crypto_wallet = CryptoWallet(
            user=other_user,
            cryptocurrency="Bitcoin",
            symbol="BTC",
            address="0x2",
            balance=100.00,
            received=300.00,
            spent=200.00,
            output_count=50,
            unspent_output_count=20,
        )
        self.crypto_wallet.save()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, '0x0')
        self.assertContains(response, '0x1')
        self.assertNotContains(response, '0x2')

    """Test Retrieve"""
    def test_valid_retrieve(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, '0x0')

    def test_invalid_retrieve(self):
        CryptoWallet.objects.all().delete()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    """Test Destroy"""
    def test_valid_destroy(self):
        wallet_count_before = CryptoWallet.objects.count()
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        wallet_count_after = CryptoWallet.objects.count()
        self.assertEqual(wallet_count_after, wallet_count_before - 1)

    def test_invalid_destroy(self):
        CryptoWallet.objects.all().delete()
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

