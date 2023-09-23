from django.core.exceptions import ValidationError
from django.test import TestCase
from accounts.models import User
from banking.models import Token
from django.utils import timezone

class TokenTestCase(TestCase):
    """Unit tests for the Token model."""

    def setUp(self):
        self.token = Token(refresh_token="48nc89q4",access_token="uch8qb91",refresh_token_expiration=timezone.now(),access_token_expiration=timezone.now())

    def test_balance_valid(self):
        self._assert_is_valid()

    def test_refresh_token_cannot_be_none(self):
        self.token.refresh_token = None
        self._assert_is_invalid()

    def test_access_token_cannot_be_none(self):
        self.token.access_token = None
        self._assert_is_invalid()

    def test_refresh_token_expiration_cannot_be_none(self):
        self.token.refresh_token_expiration = None
        self._assert_is_invalid()

    def test_access_token_expiration_cannot_be_none(self):
        self.token.access_token_expiration = None
        self._assert_is_invalid()

    def test_refresh_token_cannot_be_larger_than_1024_digits(self):
        self.token.refresh_token = "a" * 1025
        self._assert_is_invalid()

    def test_access_token_cannot_be_larger_than_1024_digits(self):
        self.token.access_token = "a" * 1025
        self._assert_is_invalid()

    def test_refresh_token_can_be_1024_digits(self):
        self.token.refresh_token = "a" * 1024
        self._assert_is_valid()

    def test_access_token_can_be_1024_digits(self):
        self.token.access_token = "a" * 1024
        self._assert_is_valid()

    def test_access_token_can_be_1024_digits(self):
        self.token.access_token = "a" * 1024
        self._assert_is_valid()

    def test_expiry_methods(self):
        self.assertTrue(self.token.refresh_expired())
        self.assertTrue(self.token.access_expired())

        previous_access_expiry =  self.token.access_token_expiration
        previous_refresh_expiry =  self.token.refresh_token_expiration

        self.token.set_refresh_expiry(86400)
        self.token.set_access_expiry(86400)

        self.assertNotEqual(self.token.access_token_expiration,previous_access_expiry)
        self.assertNotEqual(self.token.refresh_token_expiration,previous_refresh_expiry)

        self.assertFalse(self.token.refresh_expired())
        self.assertFalse(self.token.access_expired())

    def _assert_is_valid(self):
        try:
            self.token.full_clean()
        except (ValidationError):
            self.fail('Test token should be valid')

    def _assert_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.token.full_clean()