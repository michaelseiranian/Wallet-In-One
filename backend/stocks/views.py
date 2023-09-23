from django.http import JsonResponse
import plaid
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
import json
from plaid.model.country_code import CountryCode
from plaid.model.products import Products
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import generics, permissions

from .serializers import AddStockAccount, AddTransaction, AddStock
from .models import StockAccount,Transaction, Stock

from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from flask import jsonify
from plaid.model.accounts_get_request import AccountsGetRequest
from .services import setUpClient, calculate_metrics
from plaid.model.institutions_search_request import InstitutionsSearchRequest
from plaid.model.institutions_search_request_options import InstitutionsSearchRequestOptions
from plaid.model.investments_holdings_get_request import InvestmentsHoldingsGetRequest
from rest_framework import status
from plaid.model.investments_transactions_get_request import InvestmentsTransactionsGetRequest
from plaid.model.investments_transactions_get_request_options import InvestmentsTransactionsGetRequestOptions
from datetime import datetime
from datetime import timedelta
import datetime
import json
import time
from django.utils import timezone
from dateutil.relativedelta import relativedelta

@api_view(['POST'])
@csrf_exempt
def initiate_plaid_link(request):
    """
    API call to receive a Temporary Link Token that will be used to open the Plaid Link SDK on the frontend.
    """

    client = setUpClient()
    prods = ['investments', 'transactions'] # More Products can be added if desired
    products = []
    for product in prods:
        products.append(Products(product))
    
    request = LinkTokenCreateRequest(
        products=products,
        client_name="KCL",  # Name of the Plaid Account
        language='en',
        country_codes=list(map(lambda x: CountryCode(x), ['US'])), # UK does not have access to Investments Products
        user=LinkTokenCreateRequestUser(
            client_user_id=str(request.user.id)
        )
    )
    response = client.link_token_create(request)
    link_token = response['link_token']
    return Response({'link_token': link_token})



@api_view(['POST'])
def get_access_token(request):
    """
    API call to access the access token after the plaid SDK has been closed, this would then be used to access all details for the selected account.
    """
    public_token = request.data.get('public_token') # Temporary Public Token is used to exchange for the Access Token
    client = setUpClient()
    try:
        exchange_request = ItemPublicTokenExchangeRequest(
            public_token=public_token)
        exchange_response = client.item_public_token_exchange(exchange_request)
        access_token = exchange_response['access_token']
        return Response({'access_token': access_token})
    except plaid.ApiException as e:
        return Response({"Error": json.loads(e.body)}, status=400)

    
@api_view(['POST'])
def get_balance(request):
    """
    API call to get the balance of a specific stock account, specified via the access token provided in the body.
    """
    client = setUpClient()
    try:
        request = AccountsGetRequest(
            access_token=request.data.get('access_token')   # Used to identify the stock account selected by the user
        )
        response = client.accounts_get(request)
        return Response(response.to_dict())
    except plaid.ApiException as e:
        return Response({"Error": json.loads(e.body)}, status=400)
        

@api_view(['POST'])
def get_logo(request):
    """
    API call to access the logo of the instiution of the stock account selected by the user, logo will be returned and stored with base64 encoding.
    """
    client = setUpClient()
    options = InstitutionsSearchRequestOptions(include_optional_metadata=True)
    request = InstitutionsSearchRequest(
        query=request.data.get('name'),
        products=None,
        country_codes=list(map(lambda x: CountryCode(x), ['US'])),
        options=options
    )
    institution_response = client.institutions_search(request)
    if len(institution_response.institutions) != 0:
        return Response({'logo': institution_response.institutions[0].logo})
    else:
        return Response({"Error": 'Institution Does Not Exist'}, status=400)

@api_view(['POST'])
def get_stocks(request):
    """
    API call to access the stocks within the selected stock account.
    """
    client = setUpClient()
    try:
        request = InvestmentsHoldingsGetRequest(access_token=request.data.get('access_token')) # Access Token used to identify the stock account selected
        response = client.investments_holdings_get(request)
        return Response(response.to_dict())
    except plaid.ApiException as e:
        return Response({"Error": json.loads(e.body)}, status=400)
    
@api_view(['POST'])
def get_transactions(request):
    """
    API call to access the Investment Transactions for the specified stock account.
    """
    client = setUpClient()
    start_date = (datetime.datetime.now() - timedelta(days=(1000))) # Access the transactions from the last 1000 days
    end_date = datetime.datetime.now()
    try:
        options = InvestmentsTransactionsGetRequestOptions()
        request = InvestmentsTransactionsGetRequest(
            access_token=request.data.get('access_token'),
            start_date=start_date.date(),
            end_date=end_date.date(),
            options=options
        )
        response = client.investments_transactions_get(request)
        return Response(response.to_dict())
    except plaid.ApiException as e:
        return Response({"Error": json.loads(e.body)}, status=400)


class addAccount(generics.CreateAPIView):
    """
    View that deals with adding a stock account to the database
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = AddStockAccount
    queryset = StockAccount.objects.all()

class AddTransactions(generics.CreateAPIView):
    """
    View that deals with adding a transaction to the database
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = AddTransaction
    queryset = Transaction.objects.all()

@api_view(['GET'])
def listAccounts(request):
    """
    View that deals with accessing all stock accounts for the logged in user.
    """
    accounts = StockAccount.objects.filter(user=request.user)
    serializer = AddStockAccount(accounts, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def listTransactions(request,stock):
    """
    View that deals with accessing all transactions for the logged in user.
    """
    transactions = Transaction.objects.filter(stock=stock, stock__user=request.user)
    serializer = AddTransaction(transactions, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def listStocks(request, stockAccount):
    """
    View that deals with accessing all stocks for the logged in user and the specified stock account.
    """
    stocks = Stock.objects.filter(stockAccount=stockAccount, stockAccount__user=request.user)
    serializer = AddStock(stocks, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getTransaction(request, id):
    """
    View that deals with accessing a specified transaction
    """
    transaction = Transaction.objects.get(id=id)
    serializer = AddTransaction(transaction, many=False)
    return Response(serializer.data)

class addStock(generics.CreateAPIView):
    """
    View that deals with adding a stock to the database
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = AddStock
    queryset = Stock.objects.all()


@api_view(['DELETE'])
def deleteAccount(request, stockAccount):
    """
    View that deletes a single, specified stock account that belongs to the user.
    """
    if StockAccount.objects.filter(account_id=stockAccount).count() == 0:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    stock_account = StockAccount.objects.get(account_id=stockAccount)
    if stock_account.user != request.user:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    stock_account.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET'])
def getMetrics(request):
    """
    View that calculates and returns insights for the stock accounts for the current user.
    """
    metrics = {}
    # Accesses the time frame for the insights
    start1month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    start3month = start1month - relativedelta(months=3-1)
    start6month = start1month - relativedelta(months=6-1)
    start12month = start1month - relativedelta(months=12-1)

    transactions = Transaction.objects.filter(stock__user = request.user) # All transactions for the logged in user
    metrics['all'] = calculate_metrics(transactions)
    metrics['1 Month'] = calculate_metrics(transactions.filter(date__gte=start1month))
    metrics['3 Months'] = calculate_metrics(transactions.filter(date__gte=start3month))
    metrics['6 Months'] = calculate_metrics(transactions.filter(date__gte=start6month))
    metrics['12 Months'] = calculate_metrics(transactions.filter(date__gte=start12month))

    return Response(metrics)

@api_view(['GET'])
def getAccount(request, account_id):
    """
    View that deals with accessing a specified stock account
    """
    account = StockAccount.objects.get(account_id=account_id)
    return Response({'access_token': account.access_token, 'logo': account.institution_logo, 'balance': account.balance.amount, 'institution_name': account.institution_name, 'name': account.name})