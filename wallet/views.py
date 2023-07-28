from decimal import Decimal

from rest_framework import generics
from rest_framework.response import Response

from wallet.models import Wallet
from wallet.models.wallet import generate_wallet_name
from wallet.serializers import WalletSerializer, WalletCreateSerializer


class WalletListCreateView(generics.ListCreateAPIView):
    queryset = Wallet.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return WalletSerializer
        if self.request.method == "POST":
            return WalletCreateSerializer

    def create(self, request, *args, **kwargs):
        user_wallets_count = Wallet.objects.filter().count()
        if user_wallets_count >= 5:
            return Response(
                {"error": "Вы создали максимальное количество кошельков"}, status=400
            )

        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        wallet_name = generate_wallet_name()
        currency = self.request.data.get("currency")
        if currency == "USD" or currency == "EUR":
            balance = Decimal("3.00")
        elif currency == "RUB":
            balance = Decimal("100.00")
        serializer.save(name=wallet_name, balance=balance)


class WalletDetailView(generics.RetrieveDestroyAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    lookup_field = "name"
