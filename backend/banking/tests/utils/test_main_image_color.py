from io import BytesIO
from django.test import TestCase, Client
from banking.util import main_image_color
from unittest.mock import Mock, patch
from PIL import Image

def generate_mock(test_image):
    image_bytes = BytesIO()
    test_image.save(image_bytes, format='PNG')
    image_bytes.seek(0)
    
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.content = image_bytes.getvalue()
    return mock_response

class MainImageColorTestCase(TestCase):

    @patch('requests.get')
    def test_main_image_color(self, mock_get):
        # Create a test image where dominant color is red
        test_image = Image.new('RGBA', (30, 30), color=(255, 0, 0))
        mock_get.return_value = generate_mock(test_image)
        self.assertEqual(main_image_color('https://example.com/red'),'#FF0000')

    @patch('requests.get')
    def test_image_with_multiple_colors(self, mock_get):
        test_image = Image.new('RGBA', (2, 2), color=(255, 0, 0)) # Fully red image

        # Make all pixels except 1 blue
        test_image.putpixel((0, 0), (0, 255, 0))
        test_image.putpixel((0, 1), (0, 255, 0))
        test_image.putpixel((1, 0), (0, 255, 0))

        mock_get.return_value = generate_mock(test_image)
        self.assertEqual(main_image_color('https://example.com/mixed'),'#00FF00')

        
    @patch('requests.get')
    def test_image_only_white(self, mock_get):
        test_image = Image.new('RGBA', (30, 30), color=(255, 255, 255)) 

        mock_get.return_value = generate_mock(test_image)
        self.assertEqual(main_image_color('https://example.com/white'),'#BEBEBE')

    @patch('requests.get')
    def test_image_ignores_whitish_colors(self, mock_get):
        test_image = Image.new('RGBA', (30, 30), color=(230, 230, 230))

        # Make 1 pixel blue
        test_image.putpixel((0, 0), (0, 255, 0))

        mock_get.return_value = generate_mock(test_image)
        self.assertEqual(main_image_color('https://example.com/whitish'),'#00FF00')