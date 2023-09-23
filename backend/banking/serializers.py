from rest_framework import serializers
from .models import Account, Transaction
from .services import get_account_data, get_account_details, get_institution, account_balance
from djmoney.contrib.django_rest_framework import MoneyField
from .util import main_image_color

class URLSerializer(serializers.Serializer):
    url = serializers.URLField()

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'

    def to_representation(self, instance):
        if instance.color == '':
            instance.color = main_image_color(instance.institution_logo)
            instance.save()

        representation = super().to_representation(instance)

        representation.update({
            'balance': format_money(account_balance(instance)),
        })

        return representation

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.update({
            'formatted_amount': format_money(instance.amount)
        })
        return representation

def format_money(money):
    return {'string':str(money),'currency':str(money.currency),'amount':str(money.amount)}