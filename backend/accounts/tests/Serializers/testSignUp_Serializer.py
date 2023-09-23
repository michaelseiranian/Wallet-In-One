"""Sign up serializer unit tests"""
from django.test import TestCase
from rest_framework import serializers
from ...serializers import SignUpSerializer

class SignUpSerializerTestCase(TestCase):
    """Sign up serializer unit tests"""

    def setUp(self):
        self.serializer_input = {
            'username': '@user',
            'first_name': 'Name',
            'last_name': 'Lastname',
            'email': 'namelastname@example.org',
            'new_password': 'Password123!',
            'password_confirmation': 'Password123!'
        }

    def test_valid_data_sign_up_serializer(self):
        serializer = SignUpSerializer(data=self.serializer_input)
        self.assertTrue(serializer.is_valid())

    def test_necessary_fields_in_sign_up_serializer(self):
        serializer = SignUpSerializer()
        self.assertIn('first_name', serializer.fields)
        self.assertIn('last_name', serializer.fields)
        self.assertIn('email', serializer.fields)
        email_field = serializer.fields['email']
        self.assertTrue(isinstance(email_field, serializers.EmailField))
        self.assertIn('new_password', serializer.fields)
        self.assertIn('password_confirmation', serializer.fields)

    def test_form_uses_model_validation(self):
        self.serializer_input['email'] = 'bademail'
        serializer = SignUpSerializer(data=self.serializer_input)
        self.assertFalse(serializer.is_valid())

    def test_password_must_contain_uppercase(self):
        self.serializer_input['new_password'] = 'password123!'
        self.serializer_input['password_confirmation'] = 'password123!'
        serializer = SignUpSerializer(data=self.serializer_input)
        self.assertFalse(serializer.is_valid())

    def test_password_must_contain_lowercase(self):
        self.serializer_input['new_password'] = 'PASSWORD123!'
        self.serializer_input['password_confirmation'] = 'PASSWORD123!'
        serializer = SignUpSerializer(data=self.serializer_input)
        self.assertFalse(serializer.is_valid())

    def test_password_must_contain_number(self):
        self.serializer_input['new_password'] = 'Password!'
        self.serializer_input['password_confirmation'] = 'Password!'
        serializer = SignUpSerializer(data=self.serializer_input)
        self.assertFalse(serializer.is_valid())

    def test_password_must_contain_special_char(self):
        self.serializer_input['new_password'] = 'Password123'
        self.serializer_input['password_confirmation'] = 'Password123'
        serializer = SignUpSerializer(data=self.serializer_input)
        self.assertFalse(serializer.is_valid())

    def test_passwords_must_match(self):
        self.serializer_input['new_password'] = 'Password123!'
        self.serializer_input['password_confirmation'] = 'WrongPassword123!'
        serializer = SignUpSerializer(data=self.serializer_input)
        self.assertFalse(serializer.is_valid())