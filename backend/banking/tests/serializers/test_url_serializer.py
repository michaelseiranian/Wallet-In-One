from django.test import TestCase
from rest_framework import serializers
from banking.serializers import URLSerializer
from rest_framework.exceptions import ValidationError

class URLSerializerTestCase(TestCase):
    """URL serializer unit tests"""

    def setUp(self):
        self.input = {'url':'https://example.com'}
        self.invalid_input = {'url': 'invalid_url'}

    def test_serializer(self):
        serializer = URLSerializer(data=self.input)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['url'], 'https://example.com')

    def test_invalid_data(self):
        serializer = URLSerializer(data=self.invalid_input)
        self.assertFalse(serializer.is_valid())
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)