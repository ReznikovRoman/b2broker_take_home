from __future__ import annotations

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, permissions, viewsets
from rest_framework.filters import SearchFilter
from rest_framework_json_api.filters import OrderingFilter

from b2broker.api.pagination import SmallResultsSetPagination
from b2broker.api.views import MultiSerializerViewSetMixin
from b2broker.billings.models import Transaction, Wallet

from .serializers import TransactionListSerializer, WalletSerializer


class WalletViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """Viewset for working with crypto wallets."""

    queryset = Wallet.objects.order_by("-created_at")
    serializer_class = WalletSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["label"]
    ordering_fields = ["balance"]
    pagination_class = SmallResultsSetPagination
    http_method_names = ["get", "post", "patch"]


class TransactionViewSet(
    MultiSerializerViewSetMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """Viewset for working with transactions."""

    queryset = Transaction.objects.select_related("wallet").order_by("-created_at")
    serializer_class = TransactionListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ["txid"]
    filterset_fields = ["wallet"]
    pagination_class = SmallResultsSetPagination
    http_method_names = ["get", "post"]
