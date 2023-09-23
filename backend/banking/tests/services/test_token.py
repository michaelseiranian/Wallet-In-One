from django.test import TestCase
from banking.services import refresh_access_token, new_refresh_token, generate_tokens, get_access_token, get_requisitions
from banking.models import Token
from unittest.mock import patch
from django.utils import timezone

class TokenTestCase(TestCase):
    def test_new_refresh_token(self):
        token = new_refresh_token()
        self.assertIsNotNone(token)
        self.assertIsInstance(token, str)
        self.assertRegex(token, r'^[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_]+$')

    @patch('banking.services.credentials', { "secret_id": "", "secret_key": "" })
    def test_new_refresh_token_error(self):
        token = new_refresh_token()
        self.assertIsNone(token)

    @patch('banking.services.credentials', { "secret_id": "", "secret_key": "" })
    def test_generate_token(self):
        response = generate_tokens()
        self.assertEqual(response,{'secret_id': ['This field may not be blank.'], 'secret_key': ['This field may not be blank.'], 'status_code': 400})
    
    def test_refresh_access_token(self):
        response = refresh_access_token('token')
        self.assertEqual(response,{'summary': 'Invalid token', 'detail': 'Token is invalid or expired', 'status_code': 401})

    def test_get_access_token(self):
        t = Token(refresh_token="48nc89q4",access_token="uch8qb91",refresh_token_expiration=timezone.now(),access_token_expiration=timezone.now())
        t.save()

        token = get_access_token(True)
        self.assertIsNotNone(token)
        self.assertIsInstance(token, str)
        self.assertRegex(token, r'^[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_]+$')

    def test_get_access_token_when_refresh_not_expired(self):
        t = Token(refresh_token="48nc89q4",access_token="uch8qb91",refresh_token_expiration=timezone.now(),access_token_expiration=timezone.now())
        t.set_refresh_expiry(84600)
        t.save()
        token = get_access_token(True)
        self.assertIsNotNone(token)
        self.assertIsInstance(token, str)
        self.assertRegex(token, r'^[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_]+$')

    def test_get_access_token_when_refresh_not_expired_and_last_token_was_valid(self):
        last_token = get_access_token(True)
        token = Token.objects.all().first()
        token = get_access_token(True)
        self.assertIsNotNone(token)
        self.assertIsInstance(token, str)
        self.assertRegex(token, r'^[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_]+$')

    def test_request_generates_new_token_if_invalid(self):
        get_access_token(True)
        token = Token.objects.all().first()
        token.access_token = 'invalidid'
        token.save()

        #Make a request which uses auth request
        get_requisitions('id')

        token = Token.objects.all().first()
        self.assertIsNotNone(token.access_token)
        self.assertIsInstance(token.access_token, str)
        self.assertRegex(token.access_token, r'^[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_]+$')
