from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from django.urls import reverse
from accounts.models import User
from banking.models import Account, Transaction
from rest_framework import status
from unittest.mock import patch
from datetime import datetime

class MetricsViewTestCase(TestCase):
    
    fixtures = [
        'accounts/fixtures/user.json',
        'banking/tests/fixtures/bank_data.json'
    ]

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.get(id=1) 
        self.user2 = User.objects.get(id=3) 

        # Test the data stored in the database
        for a in Account.objects.all():
            a.last_update = timezone.now()
            a.save()

    def test_url(self):
        self.client.force_authenticate(self.user)
        self.url = reverse('metrics')
        self.assertEqual(self.url,'/banking/metrics/')

    @patch('django.utils.timezone.now')
    def test_response_from_all_accounts_from_user(self, mock_timezone):
        dt = datetime(2010, 1, 1, tzinfo=timezone.utc)
        mock_timezone.return_value = dt
        self.client.force_authenticate(self.user)
        self.url = reverse('metrics')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected =  """b\'{"1 month start":"2010-01-01T00:00:00Z","3 month start ":"2009-11-01T00:00:00Z","6 month start":"2009-08-01T00:00:00Z","12 month start":"2009-02-01T00:00:00Z","all":{"positive":{"total_amount_of_transactions":4,"highest_transaction":200.0,"lowest_transaction":100.0,"average_transaction":125.0,"variance":1875.0,"standard_deviation":43.3012701892219,"bar_data":{"labels":["December","January","February"],"values":[100.0,300.0,100.0],"data":{"2023-02-01":100.0,"2023-01-01":300.0,"2022-12-01":100.0}},"net":500.0},"negative":{"total_amount_of_transactions":3,"highest_transaction":-50.0,"lowest_transaction":-50.0,"average_transaction":-50.0,"variance":0,"standard_deviation":0,"bar_data":{"labels":["December","January","February"],"values":[-50.0,-50.0,-50.0],"data":{"2023-02-01":-50.0,"2023-01-01":-50.0,"2022-12-01":-50.0}},"net":-150.0},"both":{"total_amount_of_transactions":7,"highest_transaction":200.0,"lowest_transaction":-50.0,"average_transaction":50.0,"variance":8571.42857142857,"standard_deviation":92.5820099772551,"bar_data":{"labels":["December","January","February"],"values":[50.0,250.0,50.0],"data":{"2023-02-01":50.0,"2023-01-01":250.0,"2022-12-01":50.0}},"net":350.0},"balance_history":{"2023-02-15":100.0,"2023-02-01":150.0,"2023-01-15":50.0,"2023-01-01":100.0,"2022-12-15":-200.0,"2022-12-01":-150.0},"highest_balance":150.0,"lowest_balance":-200.0,"total_money_in":500.0,"total_money_out":-150.0,"net":350.0},"1month":{"positive":{"total_amount_of_transactions":4,"highest_transaction":200.0,"lowest_transaction":100.0,"average_transaction":125.0,"variance":1875.0,"standard_deviation":43.3012701892219,"bar_data":{"labels":["01","01","01"],"values":[100.0,300.0,100.0],"data":{"2023-02-01":100.0,"2023-01-01":300.0,"2022-12-01":100.0}},"net":500.0},"negative":{"total_amount_of_transactions":3,"highest_transaction":-50.0,"lowest_transaction":-50.0,"average_transaction":-50.0,"variance":0,"standard_deviation":0,"bar_data":{"labels":["15","15","15"],"values":[-50.0,-50.0,-50.0],"data":{"2023-02-15":-50.0,"2023-01-15":-50.0,"2022-12-15":-50.0}},"net":-150.0},"both":{"total_amount_of_transactions":7,"highest_transaction":200.0,"lowest_transaction":-50.0,"average_transaction":50.0,"variance":8571.42857142857,"standard_deviation":92.5820099772551,"bar_data":{"labels":["01","15","01","15","01","15"],"values":[100.0,-50.0,300.0,-50.0,100.0,-50.0],"data":{"2023-02-15":-50.0,"2023-02-01":100.0,"2023-01-15":-50.0,"2023-01-01":300.0,"2022-12-15":-50.0,"2022-12-01":100.0}},"net":350.0},"balance_history":{"2023-02-15":100.0,"2023-02-01":150.0,"2023-01-15":50.0,"2023-01-01":100.0,"2022-12-15":-200.0,"2022-12-01":-150.0},"highest_balance":150.0,"lowest_balance":-200.0,"total_money_in":500.0,"total_money_out":-150.0,"net":350.0},"3month":{"positive":{"total_amount_of_transactions":4,"highest_transaction":200.0,"lowest_transaction":100.0,"average_transaction":125.0,"variance":1875.0,"standard_deviation":43.3012701892219,"bar_data":{"labels":["December","January","February"],"values":[100.0,300.0,100.0],"data":{"2023-02-01":100.0,"2023-01-01":300.0,"2022-12-01":100.0}},"net":500.0},"negative":{"total_amount_of_transactions":3,"highest_transaction":-50.0,"lowest_transaction":-50.0,"average_transaction":-50.0,"variance":0,"standard_deviation":0,"bar_data":{"labels":["December","January","February"],"values":[-50.0,-50.0,-50.0],"data":{"2023-02-01":-50.0,"2023-01-01":-50.0,"2022-12-01":-50.0}},"net":-150.0},"both":{"total_amount_of_transactions":7,"highest_transaction":200.0,"lowest_transaction":-50.0,"average_transaction":50.0,"variance":8571.42857142857,"standard_deviation":92.5820099772551,"bar_data":{"labels":["December","January","February"],"values":[50.0,250.0,50.0],"data":{"2023-02-01":50.0,"2023-01-01":250.0,"2022-12-01":50.0}},"net":350.0},"balance_history":{"2023-02-15":100.0,"2023-02-01":150.0,"2023-01-15":50.0,"2023-01-01":100.0,"2022-12-15":-200.0,"2022-12-01":-150.0},"highest_balance":150.0,"lowest_balance":-200.0,"total_money_in":500.0,"total_money_out":-150.0,"net":350.0},"6month":{"positive":{"total_amount_of_transactions":4,"highest_transaction":200.0,"lowest_transaction":100.0,"average_transaction":125.0,"variance":1875.0,"standard_deviation":43.3012701892219,"bar_data":{"labels":["December","January","February"],"values":[100.0,300.0,100.0],"data":{"2023-02-01":100.0,"2023-01-01":300.0,"2022-12-01":100.0}},"net":500.0},"negative":{"total_amount_of_transactions":3,"highest_transaction":-50.0,"lowest_transaction":-50.0,"average_transaction":-50.0,"variance":0,"standard_deviation":0,"bar_data":{"labels":["December","January","February"],"values":[-50.0,-50.0,-50.0],"data":{"2023-02-01":-50.0,"2023-01-01":-50.0,"2022-12-01":-50.0}},"net":-150.0},"both":{"total_amount_of_transactions":7,"highest_transaction":200.0,"lowest_transaction":-50.0,"average_transaction":50.0,"variance":8571.42857142857,"standard_deviation":92.5820099772551,"bar_data":{"labels":["December","January","February"],"values":[50.0,250.0,50.0],"data":{"2023-02-01":50.0,"2023-01-01":250.0,"2022-12-01":50.0}},"net":350.0},"balance_history":{"2023-02-15":100.0,"2023-02-01":150.0,"2023-01-15":50.0,"2023-01-01":100.0,"2022-12-15":-200.0,"2022-12-01":-150.0},"highest_balance":150.0,"lowest_balance":-200.0,"total_money_in":500.0,"total_money_out":-150.0,"net":350.0}}\'"""
        self.assertEqual(str(response.content), expected)

    @patch('django.utils.timezone.now')
    def test_user_with_no_accounts(self, mock_timezone):
        dt = datetime(2010, 1, 1, tzinfo=timezone.utc)
        mock_timezone.return_value = dt
        self.client.force_authenticate(self.user2)
        self.url = reverse('metrics')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected =  """b\'{"1 month start":"2010-01-01T00:00:00Z","3 month start ":"2009-11-01T00:00:00Z","6 month start":"2009-08-01T00:00:00Z","12 month start":"2009-02-01T00:00:00Z","all":{"positive":{"total_amount_of_transactions":0,"highest_transaction":0,"lowest_transaction":0,"average_transaction":0,"variance":0,"standard_deviation":0,"bar_data":{"labels":[],"values":[],"data":{}},"net":null},"negative":{"total_amount_of_transactions":0,"highest_transaction":0,"lowest_transaction":0,"average_transaction":0,"variance":0,"standard_deviation":0,"bar_data":{"labels":[],"values":[],"data":{}},"net":null},"both":{"total_amount_of_transactions":0,"highest_transaction":0,"lowest_transaction":0,"average_transaction":0,"variance":0,"standard_deviation":0,"bar_data":{"labels":[],"values":[],"data":{}},"net":null},"balance_history":{},"highest_balance":0,"lowest_balance":0,"total_money_in":0,"total_money_out":0,"net":null},"1month":{"positive":{"total_amount_of_transactions":0,"highest_transaction":0,"lowest_transaction":0,"average_transaction":0,"variance":0,"standard_deviation":0,"bar_data":{"labels":[],"values":[],"data":{}},"net":null},"negative":{"total_amount_of_transactions":0,"highest_transaction":0,"lowest_transaction":0,"average_transaction":0,"variance":0,"standard_deviation":0,"bar_data":{"labels":[],"values":[],"data":{}},"net":null},"both":{"total_amount_of_transactions":0,"highest_transaction":0,"lowest_transaction":0,"average_transaction":0,"variance":0,"standard_deviation":0,"bar_data":{"labels":[],"values":[],"data":{}},"net":null},"balance_history":{},"highest_balance":0,"lowest_balance":0,"total_money_in":0,"total_money_out":0,"net":null},"3month":{"positive":{"total_amount_of_transactions":0,"highest_transaction":0,"lowest_transaction":0,"average_transaction":0,"variance":0,"standard_deviation":0,"bar_data":{"labels":[],"values":[],"data":{}},"net":null},"negative":{"total_amount_of_transactions":0,"highest_transaction":0,"lowest_transaction":0,"average_transaction":0,"variance":0,"standard_deviation":0,"bar_data":{"labels":[],"values":[],"data":{}},"net":null},"both":{"total_amount_of_transactions":0,"highest_transaction":0,"lowest_transaction":0,"average_transaction":0,"variance":0,"standard_deviation":0,"bar_data":{"labels":[],"values":[],"data":{}},"net":null},"balance_history":{},"highest_balance":0,"lowest_balance":0,"total_money_in":0,"total_money_out":0,"net":null},"6month":{"positive":{"total_amount_of_transactions":0,"highest_transaction":0,"lowest_transaction":0,"average_transaction":0,"variance":0,"standard_deviation":0,"bar_data":{"labels":[],"values":[],"data":{}},"net":null},"negative":{"total_amount_of_transactions":0,"highest_transaction":0,"lowest_transaction":0,"average_transaction":0,"variance":0,"standard_deviation":0,"bar_data":{"labels":[],"values":[],"data":{}},"net":null},"both":{"total_amount_of_transactions":0,"highest_transaction":0,"lowest_transaction":0,"average_transaction":0,"variance":0,"standard_deviation":0,"bar_data":{"labels":[],"values":[],"data":{}},"net":null},"balance_history":{},"highest_balance":0,"lowest_balance":0,"total_money_in":0,"total_money_out":0,"net":null}}\'"""
        self.assertEqual(str(response.content), expected)


