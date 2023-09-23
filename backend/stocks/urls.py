from django.urls import path

from .views import initiate_plaid_link, addAccount, listAccounts, get_access_token, get_balance,listTransactions, get_transactions,AddTransactions, get_stocks, deleteAccount, addStock
from .views import getTransaction, listStocks, get_logo, getMetrics, getAccount

urlpatterns = [
    path('initiate_plaid_link/', initiate_plaid_link, name='initiate_plaid_link'),
    path('add_stock_account/', addAccount.as_view(), name='add_stock_account'),
    path('list_accounts/', listAccounts, name='list_accounts'),
    path('get_access_token/', get_access_token, name='get_access_token'),
    path('get_balance/', get_balance, name='get_balance'),
    path('get_transactions/', get_transactions, name='get_transactions'),
    path('list_transactions/<str:stock>/', listTransactions, name='list_transactions'),
    path('add_transaction_account/', AddTransactions.as_view(), name='add_transaction_account'),
    path('get_stocks/', get_stocks, name='get_stocks'),
    path('delete_account/<str:stockAccount>/', deleteAccount, name='delete_account_stocks'),
    path('get_transaction/<str:id>/', getTransaction, name='getTransaction'),
    path('add_stock/', addStock.as_view(), name='add_stock'),
    path('list_stocks/<str:stockAccount>/', listStocks, name='list_stocks'),
    path('get_logo/', get_logo, name='get_logo'),
    path('get_metrics/', getMetrics, name='get_stock_metrics'),
    path('get_account/<str:account_id>/', getAccount, name='get_stock_account')
]