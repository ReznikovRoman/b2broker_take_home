from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from django.conf import settings

from b2broker.billings.models import Transaction

if TYPE_CHECKING:
    from tests.unit.testlib import DRFClient

pytestmark = [pytest.mark.django_db]


def test_list_ok(api: DRFClient, transactions: list[Transaction]) -> None:
    """List of transactions is paginated and each wallet is correctly serialized."""
    latest_transaction = Transaction.objects.latest("id")

    response = api.get("/api/v1/billings/transactions")

    assert response["data"][0]["id"] == str(latest_transaction.id)
    assert response["data"][0]["attributes"]["amount"] == f"{latest_transaction.amount:.18f}"
    assert response["meta"]["pagination"]["count"] == settings.DEFAULT_SMALL_PAGE_SIZE + 1
    assert "links" in response


def test_retrieve_ok(api: DRFClient, transaction: Transaction) -> None:
    """Detailed transaction info is serialized correctly."""
    response = api.get(f"/api/v1/billings/transactions/{transaction.id}")

    assert response["data"]["id"] == str(transaction.id)
    assert response["data"]["attributes"]["amount"] == f"{transaction.amount:.18f}"
    assert response["data"]["attributes"]["txid"] == transaction.txid
    assert response["data"]["attributes"]["created_at"] == transaction.created_at.astimezone().isoformat()
