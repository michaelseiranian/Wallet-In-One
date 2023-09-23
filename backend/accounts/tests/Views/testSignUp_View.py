"""Tests for the sign up view"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

class SignUpViewTestCase(TestCase):
    """Tests for the sign up view"""

    def setUp(self):
        self.client = Client()
        self.url = reverse('sign_up')
        self.serializer1_input = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'johndoe@example.com',
            'new_password': 'Test@123',
            'password_confirmation': 'Test@123'
        }
        self.serializer2_input = {
            'first_name': 'Peter',
            'last_name': 'Parker',
            'username': 'peterparker',
            'email': 'peterparker@example.com',
            'new_password': 'Test@123',
            'password_confirmation': 'Test@123'
        }

    def test_successful_sign_up(self):
        response = self.client.post(self.url, data=self.serializer1_input)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(get_user_model().objects.count(), 1)
        self.assertEqual(get_user_model().objects.get().username, 'johndoe')

    def test_unsuccessful_sign_up(self):
        self.serializer1_input['new_password'] = 'testingtesting123'
        response = self.client.post(self.url, data=self.serializer1_input)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(get_user_model().objects.count(), 0)
        self.assertEqual(response.data['new_password'], ['Password must contain an uppercase character, a lowercase character, a number and a special character.'])

    def test_sign_up_multiple_users(self):
        response = self.client.post(self.url, data=self.serializer1_input)
        response2 = self.client.post(self.url, data=self.serializer2_input)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response2.status_code, 201)
        self.assertEqual(get_user_model().objects.count(), 2)
    
    def test_signup_not_matching_passwords(self):
        self.serializer1_input['password_confirmation'] = 'Test@1234'
        response = self.client.post(self.url, data=self.serializer1_input)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(get_user_model().objects.count(), 0)
        self.assertEqual(response.data['new_password'], ["Password fields didn't match."])

    def test_signup_already_existing_email(self):
        response = self.client.post(self.url, data=self.serializer1_input)
        self.serializer2_input['email'] = 'johndoe@example.com'
        response2 = self.client.post(self.url, data=self.serializer2_input)
        self.assertEqual(response2.status_code, 400)
        self.assertEqual(get_user_model().objects.count(), 1)
        self.assertEqual(response2.data['email'], ['This field must be unique.'])

    def test_signup_already_existing_username(self):
        response = self.client.post(self.url, data=self.serializer1_input)
        self.serializer2_input['username'] = 'johndoe'
        response2 = self.client.post(self.url, data=self.serializer2_input)
        self.assertEqual(response2.status_code, 400)
        self.assertEqual(get_user_model().objects.count(), 1)
        self.assertEqual(response2.data['username'], ['user with this username already exists.'])

    def test_signup_already_existing_first_name(self):
        response = self.client.post(self.url, data=self.serializer1_input)
        self.serializer2_input['first_name'] = 'John'
        response2 = self.client.post(self.url, data=self.serializer2_input)
        self.assertEqual(response2.status_code, 201)
        self.assertEqual(get_user_model().objects.count(), 2)

    def test_signup_already_existing_last_name(self):
        response = self.client.post(self.url, data=self.serializer1_input)
        self.serializer2_input['last_name'] = 'Doe'
        response2 = self.client.post(self.url, data=self.serializer2_input)
        self.assertEqual(response2.status_code, 201)
        self.assertEqual(get_user_model().objects.count(), 2)