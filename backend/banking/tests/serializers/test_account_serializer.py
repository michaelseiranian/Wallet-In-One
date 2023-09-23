from django.test import TestCase
from accounts.models import User
from banking.models import Account
from banking.serializers import AccountSerializer
from unittest.mock import patch, Mock
from django.utils import timezone
from djmoney.money import Money
from banking.services import account_balance
from io import BytesIO
from PIL import Image
from django.utils import timezone

def generate_mock():
    test_image = Image.new('RGBA', (30, 30), color=(255, 0, 0))
    image_bytes = BytesIO()
    test_image.save(image_bytes, format='PNG')
    image_bytes.seek(0)
    
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.content = image_bytes.getvalue()
    return mock_response


class AccountSerializerTest(TestCase):
    fixtures = [
        'accounts/fixtures/user.json',
        'banking/tests/fixtures/bank_data.json'
    ]

    def setUp(self):
        self.user = User.objects.get(id=1) 
        for a in Account.objects.all():
            a.last_update = timezone.now()
            a.save()
        self.account = Account.objects.get(id='abc')
        
    def test_account_serializer(self):
        serializer = AccountSerializer(self.account)
        self.assertEqual(serializer.data['id'],'abc' )
        self.assertEqual(serializer.data['iban'],'1234' )
        self.assertEqual(serializer.data['requisition_id'],'None' )
        self.assertEqual(serializer.data['institution_name'],'Revolut' )
        self.assertEqual(serializer.data['institution_id'],'REVOLUT_REVOGB21' )
        self.assertEqual(serializer.data['institution_logo'],'https://cdn.nordigen.com/ais/REVOLUT_REVOGB21.png')
        self.assertEqual(serializer.data['user'],1)
        self.assertEqual(serializer.data['balance'],{'string': '£100.00', 'currency': 'GBP', 'amount': '100.00'})

    @patch('requests.get')
    def test_generates_color(self, mock_get):
        mock_get.return_value = generate_mock()
        self.account.color = ''
        self.account.save()
        serializer = AccountSerializer(self.account)
        self.assertEqual('#FF0000',serializer.data['color'])