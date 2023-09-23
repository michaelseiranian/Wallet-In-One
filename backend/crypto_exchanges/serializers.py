from rest_framework import serializers
from crypto_exchanges.models import *


# Token serializer
class TokenSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Token
        fields = ('user', 'crypto_exchange_object', 'asset', 'free_amount', 'locked_amount')

    def create(self, validated_data):
        token = Token.objects.create(
            **validated_data,
        )
        token.save()
        return token


# Crypto exchange account serializer
class CryptoExchangeAccountSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = CryptoExchangeAccount
        fields = ('user', 'crypto_exchange_name', 'api_key', 'secret_key', 'created_at')

    def create(self, validated_data):
        crypto_exchange_account = CryptoExchangeAccount.objects.create(
            **validated_data,
        )
        crypto_exchange_account.save()
        return crypto_exchange_account


# Transactions serializer
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('crypto_exchange_object', 'asset', 'transaction_type', 'amount', 'timestamp')

    def create(self, validated_data):
        transaction = Transaction.objects.create(
            **validated_data,
        )
        transaction.save()
        return transaction
