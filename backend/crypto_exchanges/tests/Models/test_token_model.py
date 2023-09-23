from django.test import TestCase
from django.core.exceptions import ValidationError
from accounts.models import User
from crypto_exchanges.models import Token, CryptoExchangeAccount


class TokenModelTestCase(TestCase):
    """Unit tests for the token model"""

    fixtures = ['accounts/fixtures/user.json']

    def setUp(self):
        super(TestCase, self).setUp()

        self.user = User.objects.get(id=1)

        self.crypto_exchange_account = CryptoExchangeAccount(
            user=self.user,
            crypto_exchange_name='Kraken',
            api_key='owibhouibh034985',
            secret_key='oefigno23487h',
        )

        self.crypto_exchange_account.save()

        self.token = Token(user=self.user,
                           crypto_exchange_object=self.crypto_exchange_account,
                           asset="ETH",
                           free_amount="5.2341",
                           locked_amount="0.2134")

    def _assert_token_is_valid(self, token):
        try:
            token.full_clean()
        except ValidationError:
            self.fail("Invalid token")

    def _assert_token_is_invalid(self, token):
        with self.assertRaises(ValidationError):
            token.full_clean()

    def test_token_user_not_blank(self):
        self.token.user = None
        self._assert_token_is_invalid(self.token)

    def test_asset_not_blank(self):
        self.token.asset = None
        self._assert_token_is_invalid(self.token)

    def test_asset_can_be_5_chars(self):
        self.token.asset = 'Q' * 5
        self._assert_token_is_valid(self.token)

    def test_asset_cannot_exceed_5_chars(self):
        self.token.asset = 'Q' * 6
        self._assert_token_is_invalid(self.token)

    def test_free_cannot_be_negative(self):
        self.token.free_amount = -1.0
        self._assert_token_is_invalid(self.token)

    def test_locked_cannot_be_negative(self):
        self.token.locked_amount = -1.0
        self._assert_token_is_invalid(self.token)

