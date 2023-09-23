from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from crypto_wallets.models import CryptoWallet, CryptoWalletTransaction
from crypto_wallets.services import CryptoWalletService, get_timestamp, normalise_value


class CryptoWalletTransactionSerializer(serializers.ModelSerializer):
    """
    Nested serializer that serializes crypto wallet transactions of a related crypto wallet.
    """

    class Meta:
        model = CryptoWalletTransaction
        fields = ('id', 'value', 'time')


class CryptoWalletSerializer(serializers.ModelSerializer):
    """
    Serializer that both serializes a crypto wallet into a list or into a single detail, or can create a crypto wallet
    using the cryptocurrency, symbol and address.
    """

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    transactions = CryptoWalletTransactionSerializer(source='cryptowallettransaction_set', many=True, required=False)

    class Meta:
        model = CryptoWallet
        fields = "__all__"
        extra_kwargs = dict(balance={'required': False},
                            received={'required': False},
                            spent={'required': False},
                            output_count={'required': False},
                            unspent_output_count={'required': False})
        validators = [UniqueTogetherValidator(
            queryset=CryptoWallet.objects.all(),
            fields=['user', 'cryptocurrency', 'address'],
            message="you have already added this address."
        )]

    def get_fields(self):
        """
        Function that decides whether to omit the transactions field depending on the context, used by the crypto wallet
        list view.
        """

        fields = super().get_fields()
        if self.context.get('exclude_transactions', False):
            fields.pop('transactions')
        return fields

    def create(self, validated_data):
        """
        Function that can create a crypto wallet, using the crypto wallet service with the cryptocurrency, symbol and
        address.
        """

        cryptocurrency = validated_data['cryptocurrency']
        crypto_wallet_service = CryptoWalletService(cryptocurrency, validated_data['address'])
        if crypto_wallet_service.type is None:
            raise serializers.ValidationError({'address': ["the cryptocurrency address could not be found."]})

        crypto_wallet = CryptoWallet.objects.create(
            **validated_data,
            balance=normalise_value(cryptocurrency, crypto_wallet_service.balance),
            received=normalise_value(cryptocurrency, crypto_wallet_service.received),
            spent=normalise_value(cryptocurrency, crypto_wallet_service.spent),
            output_count=crypto_wallet_service.output_count,
            unspent_output_count=crypto_wallet_service.unspent_output_count,
        )
        crypto_wallet.save()

        for transaction in crypto_wallet_service.transactions:
            crypto_wallet_transaction = CryptoWalletTransaction.objects.create(
                crypto_wallet=crypto_wallet,
                value=normalise_value(cryptocurrency, transaction['balance_change']),
                time=get_timestamp(transaction['time'])
            )
            crypto_wallet_transaction.save()

        return crypto_wallet
