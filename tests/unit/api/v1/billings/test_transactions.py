from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from b2broker.billings.models import Transaction
from tests.unit.api.base import BaseClientTest, NotFoundTestMixin, PaginationTestMixin

if TYPE_CHECKING:
    from tests.unit.testlib import DRFClient

pytestmark = [pytest.mark.django_db]


class TestTransactionAPI(
    PaginationTestMixin,
    NotFoundTestMixin,
    BaseClientTest[Transaction],
):
    """Tests for transactions API."""

    endpoint = "/api/v1/billings/transactions"

    not_found_endpoint = f"{endpoint}/1000"
    pagination_factory_name = "transactions"

    def test_list_ok(self, api: DRFClient, transactions: list[Transaction]) -> None:
        """List of transactions is serialized correctly."""
        latest_transaction = Transaction.objects.latest("id")

        got = api.get(self.endpoint)

        assert got["data"][0]["id"] == str(latest_transaction.id)
        assert got["data"][0]["attributes"]["amount"] == f"{latest_transaction.amount:.18f}"

    def test_retrieve_ok(self, api: DRFClient, transaction: Transaction) -> None:
        """Detailed transaction info is serialized correctly."""
        got = api.get(f"{self.endpoint}/{transaction.id}")

        assert got["data"]["id"] == str(transaction.id)
        assert got["data"]["attributes"]["amount"] == f"{transaction.amount:.18f}"
        assert got["data"]["attributes"]["txid"] == transaction.txid
        assert got["data"]["attributes"]["created_at"] == transaction.created_at.astimezone().isoformat()
