from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tests.unit.testlib import DRFClient


def test_ok(anon: DRFClient) -> None:
    """Endpoint always returns 'ok' status."""
    response = anon.get("/api/v1/misc/healthcheck")

    assert response["data"]["status"] == "ok"
