from django.contrib import admin

from .models import Transaction, Wallet


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ["label", "balance", "created_at"]
    search_fields = ["label"]
    ordering = ["-created_at"]


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ["wallet", "amount", "txid"]
    search_fields = ["txid"]
    list_filter = ["wallet"]
    ordering = ["-created_at"]
    list_select_related = ["wallet"]
