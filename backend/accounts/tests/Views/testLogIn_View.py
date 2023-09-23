"""Tests for the log in view."""
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from accounts.models import User

class LoginViewTestCase(TestCase):
    """Tests for the log in view."""

    fixtures = [
        'accounts/fixtures/user.json',
    ]

    def setUp(self):
        self.client = APIClient()
        self.url = reverse('login')

    def test_log_in_url(self):
        self.assertEqual(self.url,'/login/')

    def test_login_successful(self):
        form_input = { 'username': '@pickles', 'password': 'Password123%' }
        response = self.client.post(self.url, form_input, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)

    def test_login_multiple_users(self):
        form_input1 = { 'username': '@pickles', 'password': 'Password123%' }
        form_input2 = { 'username': '@parker', 'password': 'Password123%' }
        response = self.client.post(self.url, form_input1, format='json')
        response2 = self.client.post(self.url, form_input2, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response2.status_code, 200)
        self.assertIn('token', response.data)
        self.assertIn('token', response2.data)

    def test_login_invalid_credentials(self):
        form_input = { 'username': '@wrongusername', 'password': 'WrongPassword123%' }
        response = self.client.post(self.url, form_input, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'non_field_errors': ['Unable to log in with provided credentials.']})

    def test_login_missing_fields(self):
        form_input = { 'username': '@pickles' }
        response = self.client.post(self.url, form_input, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'password': ['This field is required.']})

    def test_login_by_inactive_user(self):
        self.user = User.objects.get(email='dillyparker@example.org')
        self.user.is_active = False
        self.user.save()
        form_input = { 'username': '@parker', 'password': 'Password123%' }
        response = self.client.post(self.url, form_input, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'non_field_errors': ['Unable to log in with provided credentials.']})

    def test_log_in_with_blank_password(self):
        form_input = { 'username': '@pickles', 'password': '' }
        response = self.client.post(self.url, form_input, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'password': ['This field may not be blank.']})

    def test_log_in_with_blank_username(self):
        form_input = { 'username': '', 'password': 'Password123%' }
        response = self.client.post(self.url, form_input, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'username': ['This field may not be blank.']})

