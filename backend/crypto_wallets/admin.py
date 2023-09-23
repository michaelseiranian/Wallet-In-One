from django.contrib import admin
from crypto_wallets.models import CryptoWallet, CryptoWalletTransaction

admin.site.register(CryptoWallet)
admin.site.register(CryptoWalletTransaction)
