from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from crypto_wallets.models import CryptoWallet
from crypto_wallets.serializers import CryptoWalletSerializer
from crypto_wallets.services import calculate_received_spent, calculate_predicted_balance, calculate_average_spend


class CryptoWalletViewSet(GenericViewSet):
    """
    View set that deals with the views relating to the list of crypto wallets and the detail of a single crypto wallet.
    """

    serializer_class = CryptoWalletSerializer

    def get_queryset(self):
        """
        Function that returns the crypto wallets belonging to the user who initiated the request.
        """

        return CryptoWallet.objects.filter(user=self.request.user)

    def create(self, request):
        """
        Function that creates a crypto wallet using the serializer and the data from the request.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        """
        Function that retrieves a list of crypto wallets belonging to a user, omitting the transaction field.
        """

        serializer = self.get_serializer(self.get_queryset(), many=True, context={'exclude_transactions': True})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        Function that retrieves a detail of a single, specified crypto wallet, including the transaction field.
        """

        crypto_wallet = self.get_object()
        serializer = self.get_serializer(crypto_wallet)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """
        Function that deletes a single, specified crypto wallet that belongs to the user.
        """

        crypto_wallet = self.get_object()
        crypto_wallet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CryptoWalletInsights(APIView):
    """
    View that displays crypto wallet insights relating to a user, including the predicted balance, received and spent,
    and the average spend.
    """

    def get(self, request):
        """
        Function that returns a list of insights that relate to a users crypto wallets.
        """

        predicted_balance = calculate_predicted_balance(self.request.user)
        received_spent = calculate_received_spent(self.request.user)
        average_spend = calculate_average_spend(self.request.user)
        return Response({'predicted_balance': predicted_balance, 'received_spent': received_spent, 'average_spend': average_spend})


class CryptoWalletUpdate(APIView):
    """
    View that updates all crypto wallets belonging to a user, updating the fields of the crypto wallet such as the
    balance, and updates the transactions.
    """

    def put(self, request):
        """
        Function that removes a crypto wallet, but re-adds the crypto wallet again, which will update the fields of the
        crypto wallet and the transactions.
        """

        wallets = CryptoWallet.objects.filter(user=self.request.user)
        for wallet in wallets:
            cryptocurrency = wallet.cryptocurrency
            symbol = wallet.symbol
            address = wallet.address
            wallet.delete()

            serializer = CryptoWalletSerializer(
                data={'cryptocurrency': cryptocurrency, 'symbol': symbol, 'address': address},
                context={'request': request}
            )
            serializer.is_valid()
            serializer.save()

        return Response(status=status.HTTP_200_OK)
