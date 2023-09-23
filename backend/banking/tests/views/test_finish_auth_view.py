from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from django.urls import reverse
from accounts.models import User
from banking.models import Account, Transaction
from rest_framework import status
from unittest.mock import Mock, patch

class FinishAuthViewTestCase(TestCase):
    
    fixtures = [
        'accounts/fixtures/user.json',
        'banking/tests/fixtures/bank_data.json'
    ]

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.get(id=1) 
        self.client.force_authenticate(self.user)
        self.url = reverse('finish_auth')
        self.invalid_data = {'url': 'https://example.com'}
        self.valid_data = {'url': 'https://ob.nordigen.com/psd2/start/ABC/REVOLUT_REVOGB21'}
        self.results = [
            {'id': '10291-12312-3123', 
            'created': '2023-01-1T18:38:26.328474Z',
            'redirect': 'https://example.com',
            'status': 'CR',
            'institution_id': 'REVOLUT_REVOGB21',
            'agreement': '',
            'reference': '1',
            'accounts': [],
            'user_language': 'EN',
            'link': 'https://ob.nordigen.com/psd2/start/ABC/REVOLUT_REVOGB21',
            'ssn': None,
            'account_selection': False,
            'redirect_immediate': False}
        ]

    def test_url(self):
        self.assertEqual(self.url,'/banking/finish_auth/')

    def test_response_without_url(self):
        response = self.client.post(self.url)
        self.assertEqual(response.content,b'{"url":["This field is required."]}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('requests.get')
    def test_response_with_invalid_url(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        def mock_json():
            return {'results': self.results}

        mock_response.json = mock_json
        mock_get.return_value = mock_response

        response = self.client.post(self.url, self.invalid_data)
        self.assertEqual(response.content,b'{"error":"Link not found"}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('requests.get')
    def test_response_with_no_accounts(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        def mock_json():
            url = mock_get.call_args[0][0]
            if 'institutions' in url:
                return {}
            else:
                return {'results': self.results}

        mock_response.json = mock_json
        mock_get.return_value = mock_response

        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.content,b'{"error":"No accounts were linked"}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('requests.get')
    def test_response_with_account_already_linked(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        self.results[0]['accounts'] = ['abc']
        def mock_json():
            url = mock_get.call_args[0][0]
            if 'institutions' in url:
                return {}
            else:
                return {'results': self.results}

        mock_response.json = mock_json
        mock_get.return_value = mock_response

        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.content,b'{"error":"The bank account(s) you attempted to link have already be added to your account"}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('requests.get')
    def test_response_with_new_and_valid_account(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        self.results[0]['accounts'] = ['new']
        def mock_json():
            url = mock_get.call_args[0][0]
            if 'accounts/new' in url:
                return {'iban':'1234'}
            elif 'institutions' in url:
                return {'id':'REVOLUT_REVOGB21','name':'Revolut','logo':'https://example.com/logo.png'}
            else:
                return {'results': self.results}

        mock_response.json = mock_json
        mock_get.return_value = mock_response

        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.content,b'[{}]')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
       
        self.assertTrue(Account.objects.filter(id='new').exists())
        new_account = Account.objects.get(id='new')
        self.assertEqual(new_account.id,'new')
        self.assertEqual(new_account.user,self.user)
        self.assertEqual(new_account.requisition_id,'10291-12312-3123')
        self.assertEqual(new_account.iban,'1234')
        self.assertEqual(new_account.institution_id,'REVOLUT_REVOGB21')
        self.assertEqual(new_account.institution_name,'Revolut')
        self.assertEqual(new_account.institution_logo,'https://example.com/logo.png')

