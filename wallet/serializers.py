from rest_framework import serializers
from wallet.models import Wallet


class WalletSerializer(serializers.ModelSerializer):
    balance = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)

    class Meta:
        model = Wallet
        fields = (
            "id",
            "name",
            "type",
            "currency",
            "balance",
            "created_on",
            "modified_on",
        )


class WalletCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = (
            "type",
            "currency",
        )
