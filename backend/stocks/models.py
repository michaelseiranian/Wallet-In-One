from django.db import models
from accounts.models import User
from djmoney.models.fields import MoneyField

# Stock Account Model, using a user as a foreign key
class StockAccount(models.Model):
    account_id = models.CharField(max_length=1024, primary_key=True, unique=True, blank=False)
    access_token = models.CharField(max_length=1024, blank=False)
    name = models.CharField(max_length=1024, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    institution_id = models.CharField(max_length=1024, blank=False)
    institution_name = models.CharField(max_length=1024, blank=False)
    balance = MoneyField(default_currency='GBP', decimal_places=2, max_digits=11)
    institution_logo = models.CharField(max_length=10000, null=True)

# Stock Model, using a stock account as a foreign key, this is what a stock account holds
class Stock(models.Model):
    stockAccount = models.ForeignKey(StockAccount, on_delete=models.CASCADE, blank=False)
    institution_price = MoneyField(default_currency='GBP', decimal_places=2, max_digits=11)
    name = models.CharField(max_length=1024, blank=False)
    ticker_symbol = models.CharField(max_length=1024, blank=False, null=True)
    quantity = models.FloatField()
    security_id = models.CharField(max_length=100, blank=False, null=False)

# Transaction Model, using a stock account as a foreign key
class Transaction(models.Model):
    stock = models.ForeignKey(StockAccount, on_delete=models.CASCADE, blank=False)
    account_id = models.CharField(max_length=100, blank=False, null=False)
    amount = models.FloatField(blank=False,null=False) #  Positive values when money moves out of the account; negative values when money moves in.
    quantity = models.FloatField(blank=False,null=False) 
    price = models.FloatField(blank=False,null=False) 
    fees = models.FloatField(blank=False,null=True) 
    latitude = models.FloatField(blank=False)
    longitude = models.FloatField(blank=False)
    iso_currency_code = models.CharField(max_length=30, blank=False, null=True)
    # Always null if unofficial_currency_code is non-null.
    unofficial_currency_code = models.CharField(max_length=100, blank=False, null=True)

    date = models.DateField(blank=False, null=False)
    datetime = models.DateTimeField(blank=True, null=True)
    authorized_date = models.DateField(blank=True, null=True)
    authorized_datetime = models.DateTimeField(blank=True, null=True)

    name = models.CharField(max_length=100, blank=False, null=False)
    merchant_name = models.CharField(max_length=50, blank=True, null=True)

    pending_transaction_id = models.CharField(max_length=100, blank=True, null=True)
    account_owner = models.CharField(max_length=50, blank=True, null=True)
    investment_transaction_id = models.CharField(max_length=100, blank=False, null=False)
    security_id = models.CharField(max_length=100, blank=False, null=False)
    transaction_code = models.CharField(
        max_length=30,
        blank=True, 
        null=True,
        choices= (
            ("adjustment", "Adjustment"), # Bank adjustment.
            ("atm", "ATM"), # Cash deposit or withdrawal via an automated teller machine.
            ("bank charge", "Bank charge"), # Charge or fee levied by the institution.
            ("bill payment", "Bill payment"), # Payment of a bill.
            ("cash", "Cash"), # Cash deposit or withdrawal.
            ("cashback", "Cashback"), # Cash withdrawal while making a debit card purchase.
            ("cheque", "Cheque"), # Document ordering the payment of money to another person or organization.
            ("direct debit", "Direct debit"), # Automatic withdrawal of funds initiated by a third party at a regular interval.
            ("interest", "Interest"), # Interest earned or incurred.
            ("purchase", "Purchase"), # Purchase made with a debit or credit card.
            ("standing order", "Standing order"), # Payment instructed by the account holder to a third party at a regular interval.
            ("transfer", "Transfer") # Transfer of money between accounts.
        )
    )


