from django.utils.timezone import now

from django.db import models
from accounts.models import User
from django.core.validators import MinValueValidator


# Crypto exchange account model
class CryptoExchangeAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crypto_exchange_name = models.CharField(max_length=255)
    api_key = models.CharField(max_length=255)
    secret_key = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


# Token model
class Token(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crypto_exchange_object = models.ForeignKey(CryptoExchangeAccount, on_delete=models.CASCADE)
    asset = models.CharField(max_length=5)
    free_amount = models.FloatField(validators=[MinValueValidator(0.0)])
    locked_amount = models.FloatField(validators=[MinValueValidator(0.0)])


# Transaction history model
class Transaction(models.Model):
    crypto_exchange_object = models.ForeignKey(CryptoExchangeAccount, on_delete=models.CASCADE)
    asset = models.CharField(max_length=15)
    transaction_type = models.CharField(max_length=20)
    amount = models.FloatField(validators=[MinValueValidator(0.0)])
    timestamp = models.DateTimeField(default=now)
