from rest_framework_json_api import serializers

from b2broker.billings.models import Transaction, Wallet


class WalletSerializer(serializers.ModelSerializer):  # type: ignore[misc]
    """Crypto wallet serializer."""

    class Meta:
        model = Wallet
        fields = ["id", "label", "balance", "created_at"]
        read_only_fields = ["balance"]


class TransactionListSerializer(serializers.ModelSerializer):  # type: ignore[misc]
    """Transaction serializer."""

    class Meta:
        model = Transaction
        fields = ["id", "wallet", "amount", "txid", "created_at"]
