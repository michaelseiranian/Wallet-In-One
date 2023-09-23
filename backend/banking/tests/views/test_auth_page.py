from django.test import TestCase, Client
from rest_framework.test import APIClient
from django.urls import reverse
from accounts.models import User
from rest_framework import status
from banking.services import delete_requisition

class AuthPageViewTestCase(TestCase):
    
    fixtures = [
        'accounts/fixtures/user.json',
    ]

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.get(id=1)  
        self.client.force_authenticate(self.user)
        self.url = reverse('auth_page',kwargs={'id':'REVOLUT_REVOGB21'})

    def test_url(self):
        self.assertEqual(self.url,'/banking/auth_page/REVOLUT_REVOGB21/')

    def test_response(self):
        response = self.client.get(self.url)
        url = response.data['url']
        id = url.split('/')[-2]
        delete_requisition(id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('url',list(response.data.keys()))

    def test_invalid_id(self):
        self.url = reverse('auth_page',kwargs={'id':'Invalid_ID'})
        response = self.client.get(self.url)
        self.assertIn('url',list(response.data.keys()))
        self.assertEqual(response.data,{'url': None})