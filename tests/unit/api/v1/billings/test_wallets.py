from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from django.conf import settings

from b2broker.billings.models import Wallet

if TYPE_CHECKING:
    from tests.unit.testlib import DRFClient

pytestmark = [pytest.mark.django_db]


def test_list_ok(api: DRFClient, wallets: list[Wallet]) -> None:
    """List of wallets is paginated and each wallet is correctly serialized."""
    latest_wallet = Wallet.objects.latest("id")

    response = api.get("/api/v1/billings/wallets")

    assert response["data"][0]["id"] == str(latest_wallet.id)
    assert response["data"][0]["attributes"]["balance"] == f"{latest_wallet.balance:.18f}"
    assert response["meta"]["pagination"]["count"] == settings.DEFAULT_SMALL_PAGE_SIZE + 1
    assert "links" in response


def test_retrieve_ok(api: DRFClient, wallet: Wallet) -> None:
    """Detailed wallet info is serialized correctly."""
    response = api.get(f"/api/v1/billings/wallets/{wallet.id}")

    assert response["data"]["id"] == str(wallet.id)
    assert response["data"]["attributes"]["balance"] == f"{wallet.balance:.18f}"
    assert response["data"]["attributes"]["label"] == wallet.label
    assert response["data"]["attributes"]["created_at"] == wallet.created_at.astimezone().isoformat()
