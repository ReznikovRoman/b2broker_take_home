import pytest

from .testlib import DRFClient


@pytest.fixture
def api() -> DRFClient:
    """Core API client."""
    return DRFClient()


@pytest.fixture
def anon() -> DRFClient:
    """API client for unauthenticated users."""
    return DRFClient(anon=True)
