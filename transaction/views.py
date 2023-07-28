from decimal import Decimal
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.response import Response

from transaction.models import Transaction
from transaction.serializers import (
    TransactionCreateSerializer,
    TransactionSerializer,
    TransactionViewSerializer,
)
from wallet.models import Wallet


class TransactionListCreateView(generics.CreateAPIView):
    serializer_class = TransactionCreateSerializer

    @transaction.atomic
    def perform_create(self, serializer):
        sender_wallet_name = self.request.data.get("sender")
        receiver_wallet_name = self.request.data.get("receiver")
        transfer_amount = Decimal(self.request.data.get("transfer_amount"))

        sender_wallet = get_object_or_404(Wallet, name=sender_wallet_name)
        receiver_wallet = get_object_or_404(Wallet, name=receiver_wallet_name)

        if sender_wallet.currency != receiver_wallet.currency:
            raise ValidationError("Пожалуйста, выберите кошельки с одинаковой валютой")

        commission = Decimal("0.0")
        if sender_wallet.user != receiver_wallet.user:
            commission = transfer_amount * Decimal("0.10")

        if sender_wallet.balance < transfer_amount + commission:
            raise ValidationError("Недостаточно средств для перевода")

        if transfer_amount < 0:
            raise ValidationError("сумма должна быть больше 0")

        sender_wallet.balance -= transfer_amount + commission
        receiver_wallet.balance += transfer_amount

        sender_wallet.save()
        receiver_wallet.save()

        transaction = serializer.save(
            sender=sender_wallet,
            receiver=receiver_wallet,
            transfer_amount=transfer_amount,
            commission=commission,
            status="PAID",
            timestamp=timezone.now(),
        )

        serializer = TransactionSerializer(transaction)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


def create_transaction(request):
    serializer = TransactionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserTransactionListAPIView(generics.ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionViewSerializer


class TransactionDetailView(generics.RetrieveAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionViewSerializer


class WalletTransactionListAPIView(generics.ListAPIView):
    serializer_class = TransactionViewSerializer

    def get_queryset(self):
        wallet_name = self.kwargs["wallet_name"]
        queryset = Transaction.objects.filter(
            sender__name=wallet_name
        ) | Transaction.objects.filter(receiver__name=wallet_name)

        if not queryset.exists():
            raise NotFound("транзакций по заданному кошельку ещё не было")

        return queryset
