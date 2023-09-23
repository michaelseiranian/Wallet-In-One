from django.db import models

from accounts.models import User


class CryptoWallet(models.Model):
    """
    Model that contains data on a crypto wallet, including the cryptocurrency of the wallet, the identifying address,
    the amount received and spent, the output counts and the transactions.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cryptocurrency = models.CharField(max_length=256)
    symbol = models.CharField(max_length=16)
    address = models.CharField(max_length=256, blank=False)
    balance = models.FloatField()
    received = models.FloatField()
    spent = models.FloatField()
    output_count = models.IntegerField()
    unspent_output_count = models.IntegerField()

    class Meta:
        unique_together = ['user', 'cryptocurrency', 'address']


class CryptoWalletTransaction(models.Model):
    """
    Model that contains data on a single transaction from a crypto wallet, including its value and the timestamp of
    the transaction.
    """

    crypto_wallet = models.ForeignKey(CryptoWallet, on_delete=models.CASCADE)
    value = models.FloatField()
    time = models.IntegerField()
