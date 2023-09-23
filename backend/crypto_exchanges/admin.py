from django.contrib import admin
from .models import *


# Register your models here.

@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'crypto_exchange_object',
        'asset',
        'free_amount',
        'locked_amount'
    ]


@admin.register(CryptoExchangeAccount)
class CryptoExchangeAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'crypto_exchange_name',
        'api_key',
        'secret_key',
        'created_at'
    ]

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'crypto_exchange_object',
        'asset',
        'transaction_type',
        'amount',
        'timestamp',
    ]

