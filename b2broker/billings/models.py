from django.db import models


class Wallet(models.Model):
    """Crypto wallet."""

    label = models.CharField(verbose_name="Label", max_length=255)
    balance = models.DecimalField(verbose_name="Balance", max_digits=30, decimal_places=18, default="0")
    created_at = models.DateTimeField(verbose_name="Created at", auto_now_add=True)

    class Meta:
        verbose_name = "Wallet"
        verbose_name_plural = "Wallets"
        constraints = [
            models.CheckConstraint(check=models.Q(balance__gte="0"), name="ck_wallet_balance_non_negative"),
        ]

    def __str__(self) -> str:
        return self.label


class Transaction(models.Model):
    """Transaction."""

    wallet = models.ForeignKey(
        "Wallet", verbose_name="Wallet",
        related_name="transactions", related_query_name="transaction",
        on_delete=models.PROTECT,
    )
    txid = models.CharField(
        verbose_name="TXID", help_text="Transaction ID from the blockchain",
        max_length=255, unique=True,
    )
    amount = models.DecimalField(verbose_name="Amount", max_digits=30, decimal_places=18)
    created_at = models.DateTimeField(verbose_name="Created at", auto_now_add=True)

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"

    def __str__(self) -> str:
        return self.txid
