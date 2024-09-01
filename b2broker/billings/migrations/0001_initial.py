import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Transaction",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("txid", models.CharField(
                    help_text="Transaction ID from the blockchain", max_length=255, unique=True, verbose_name="TXID")),
                ("amount", models.DecimalField(decimal_places=18, max_digits=30, verbose_name="Amount")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Created at")),
            ],
            options={
                "verbose_name": "Transaction",
                "verbose_name_plural": "Transactions",
            },
        ),
        migrations.CreateModel(
            name="Wallet",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("label", models.CharField(max_length=255, verbose_name="Label")),
                ("balance", models.DecimalField(decimal_places=18, max_digits=30, verbose_name="Balance")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Created at")),
            ],
            options={
                "verbose_name": "Wallet",
                "verbose_name_plural": "Wallets",
            },
        ),
        migrations.AddConstraint(
            model_name="wallet",
            constraint=models.CheckConstraint(
                check=models.Q(("balance__gte", "0")), name="ck_wallet_balance_non_negative"),
        ),
        migrations.AddField(
            model_name="transaction",
            name="wallet",
            field=models.ForeignKey(
                to="billings.wallet",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="transactions", related_query_name="transaction",
                verbose_name="Wallet",
            ),
        ),
    ]
