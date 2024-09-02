from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from django.conf import settings

from b2broker.billings.models import Wallet
from tests.unit.api.base import BaseClientTest, PaginationTestMixin

if TYPE_CHECKING:
    from tests.unit.testlib import DRFClient

pytestmark = [pytest.mark.django_db]


class TestWalletAPI(
    PaginationTestMixin,
    BaseClientTest[Wallet],
):
    """Tests for wallets API."""

    endpoint = "/api/v1/billings/wallets"

    pagination_factory_name = "wallets"

    def test_list_ok(self, api: DRFClient, wallets: list[Wallet]) -> None:
        """List of wallets is serialized correctly."""
        latest_wallet = Wallet.objects.latest("id")

        got = api.get(self.endpoint)

        assert got["data"][0]["id"] == str(latest_wallet.id)
        assert got["data"][0]["attributes"]["balance"] == f"{latest_wallet.balance:.18f}"
        assert got["meta"]["pagination"]["count"] == settings.DEFAULT_SMALL_PAGE_SIZE + 1

    def test_retrieve_ok(self, api: DRFClient, wallet: Wallet) -> None:
        """Detailed wallet info is serialized correctly."""
        got = api.get(f"{self.endpoint}/{wallet.id}")

        assert got["data"]["id"] == str(wallet.id)
        assert got["data"]["attributes"]["balance"] == f"{wallet.balance:.18f}"
        assert got["data"]["attributes"]["label"] == wallet.label
        assert got["data"]["attributes"]["created_at"] == wallet.created_at.astimezone().isoformat()
