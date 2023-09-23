from django.shortcuts import render
from accounts.models import User
from .serializers import SignUpSerializer
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.decorators import api_view
from rest_framework.response import Response

class sign_up(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = SignUpSerializer
    queryset = User.objects.all()

# Token validation for the user logged in.
@api_view(['GET'])
def validate_token(request):
    return Response({'token_valid': True})


# View for compliling all of the total balances for each wallet asset in the app.
# Used on the homescreen to display the main pie chart and bar chart.
from banking.services import total_user_balance, chart_breakdown
from crypto_wallets.services import total_user_balance_crypto, chart_breakdown_crypto
from stocks.services import total_stock_balance, chart_breakdown_stocks
from crypto_exchanges.services import CurrentMarketPriceFetcher

@api_view(['GET'])
def graph_data(request):
    data = {
        "all": []
    }
    
    bank_data = chart_breakdown(request.user)
    crypto_data = chart_breakdown_crypto(request.user)
    stock_data = chart_breakdown_stocks(request.user)
    crypto_exchanges = CurrentMarketPriceFetcher(request.user)
    crypto_data_from_exchanges = crypto_exchanges.chart_breakdown_crypto_exchanges()

    if bank_data:
        data['all'].append({"x": "Banks", "y": total_user_balance(request.user).amount})
        data['Banks'] = bank_data
    if crypto_data:
        data['all'].append({"x": "Cryptocurrency from wallets", "y": total_user_balance_crypto(request.user)})
        data['Cryptocurrency from wallets'] = crypto_data

    if stock_data:
        data['all'].append({"x": "Stock Accounts", "y": total_stock_balance(request.user).amount})
        data['Stock Accounts'] = stock_data

    if crypto_data_from_exchanges:
        data['all'].append({"x": "Cryptocurrency from exchanges", "y": crypto_exchanges.total_user_balance_crypto()})
        data['Cryptocurrency from exchanges'] = crypto_data_from_exchanges

    return Response(data)
