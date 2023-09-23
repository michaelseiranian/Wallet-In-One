from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Sum

from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import APIException
from rest_framework.views import APIView

from .services import get_institutions, create_requisition, get_requisitions, get_account_data, total_user_balance, get_institution, update_user_accounts
from .serializers import URLSerializer, TransactionSerializer, AccountSerializer, format_money
from .models import Account, Transaction
from .util import calculate_balance_history, calculate_metrics_all
from djmoney.money import Money


@api_view(['GET'])
def bank_list(request):
    return Response(get_institutions())

@api_view(['GET'])
def auth_page(request, id):
    reference = str(request.user.id) + "-" + str(timezone.now().timestamp())
    response = create_requisition(id,"https://example.com", reference)

    if ('link' in response.keys()):
        return Response({'url': response['link']})

    return Response({'url': None})

@api_view(['POST'])
def finish_auth(request):
    serializer = URLSerializer(data=request.data)
    if serializer.is_valid():
        url = serializer.validated_data['url']
        r = get_requisitions()['results']
        try:
            requisition = next(filter(lambda x: x.get('link') == url, r))
            accounts = requisition['accounts']
            institution = get_institution(requisition['institution_id'])
            
            if len(accounts) == 0:
                return Response({'error': 'No accounts were linked'}, status=400)
            else:
                accountsData = []
                for i in accounts:
                    if (not Account.objects.filter(id=i).exists()):
                        new_account = Account(id=i, user=request.user, requisition_id= requisition['id'])
                        bank_id = requisition['institution_id']

                        data = get_account_data(i)
                        new_account.iban = data['iban']
                        new_account.institution_id = institution['id']
                        new_account.institution_name = institution['name']
                        new_account.institution_logo = institution['logo']
                        new_account.save()

                        accountsData.append({})
                
                if (len(accountsData) == 0):
                    return Response({'error': 'The bank account(s) you attempted to link have already be added to your account'}, status=400)
                else:
                    return Response(accountsData)    

        except StopIteration:
            return Response({'error': 'Link not found'}, status=400)
    else:
        return Response(serializer.errors, status=400)

class AccountList(generics.ListAPIView):
    model = Account
    serializer_class = AccountSerializer

    def get_queryset(self):
        update_user_accounts(self.request.user)
        id = self.kwargs.get('account_id')
        if (id):
            return Account.objects.filter(id=id, user = self.request.user)
        else:
            return Account.objects.filter(user = self.request.user)


class TransactionList(generics.ListAPIView):
    model = Transaction
    serializer_class = TransactionSerializer

    def get_queryset(self):
        update_user_accounts(self.request.user)
        id = self.kwargs.get('account_id')
        if (id):
            return Transaction.objects.filter(account=id,account__user = self.request.user).order_by('-time')
        else:
            return Transaction.objects.filter(account__user = self.request.user).order_by('-time')

from dateutil.relativedelta import relativedelta

@api_view(['GET'])
def metrics(request, account_id=None):
    res = {}

    # Start of current month
    start1month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    start3month = start1month - relativedelta(months=3-1)
    start6month = start1month - relativedelta(months=6-1)
    start12month = start1month - relativedelta(months=12-1)


    res['1 month start'] = start1month
    # # Start of month 3 months ago
    res['3 month start '] = start3month
    # # Start of month 6 months ago
    res['6 month start'] = start6month
    # # Start of month 12 months ago
    res['12 month start'] = start12month

    #TODO: replace
    transactions = Transaction.objects.filter(account__user = request.user, amount_currency="GBP")
    #transactions = Transaction.objects.filter(account=Account.objects.all()[2], account__user = request.user, amount_currency="GBP")

    #balance = Account.objects.all()[2].account_balance() #TODO :remove
    balance = total_user_balance(request.user)

    res['all'] = calculate_metrics_all(transactions,balance)
    res['1month'] = calculate_metrics_all(transactions.filter(time__gte=start1month),balance,'day')
    res['3month'] = calculate_metrics_all(transactions.filter(time__gte=start3month),balance)
    res['6month'] = calculate_metrics_all(transactions.filter(time__gte=start6month),balance)
    return Response(res)    
    

@api_view(['GET'])
def delete_account(request, account_id):
    Account.objects.filter(user=request.user, id=account_id).delete()
    return Response({'Success': 'Deleted'}, status=200)
