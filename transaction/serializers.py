from rest_framework import serializers
from transaction.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = (
            "id",
            "sender",
            "receiver",
            "transfer_amount",
            "commission",
            "status",
            "timestamp",
        )


class TransactionCreateSerializer(serializers.ModelSerializer):
    sender = serializers.CharField()
    receiver = serializers.CharField()
    transfer_amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Transaction
        fields = (
            "sender",
            "receiver",
            "transfer_amount",
        )


class TransactionViewSerializer(serializers.ModelSerializer):
    sender = serializers.CharField()
    receiver = serializers.CharField()

    class Meta:
        model = Transaction
        fields = (
            "id",
            "sender",
            "receiver",
            "transfer_amount",
            "commission",
            "status",
            "timestamp",
        )
