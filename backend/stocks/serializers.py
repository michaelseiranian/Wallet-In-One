from rest_framework import serializers

from .models import StockAccount,Transaction, Stock

from rest_framework.fields import CurrentUserDefault

class AddStockAccount(serializers.ModelSerializer):
    """
    Serializer that is used for Stock Accounts
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault()) # Accesses the user that has accessed this serializer
    class Meta:
        model = StockAccount
        fields = '__all__'

    """
    Ensures that adding the same stock account by the same user is not valid
    """
    def validate(self, attrs):
        super().validate(attrs)
        if StockAccount.objects.filter(name=attrs['name'], institution_id=attrs['institution_id'], user=attrs['user']).exists():
            raise serializers.ValidationError('Account already exists')
        return attrs

    def create(self, validated_data):
        account = StockAccount.objects.create(**validated_data)
        account.save()
        return account
    

# Serializer used for Investment Transactions, uses all the fields in the model
class AddTransaction(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

# Serializer used for Stocks, uses all the fields in the model
class AddStock(serializers.ModelSerializer):

    class Meta:
       model = Stock
       fields = '__all__'


