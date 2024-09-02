from __future__ import annotations

from typing import TYPE_CHECKING, Any, TypeVar, cast

import pytest

from django.conf import settings

if TYPE_CHECKING:
    from collections.abc import Mapping

    from _pytest.fixtures import FixtureRequest

    from django.db.models import Model

    from tests.unit.testlib import DRFClient

    T = TypeVar("T", bound=Model)

pytestmark = [pytest.mark.django_db]


class BaseClientTest[T: Model]:
    """Base test class."""

    client: DRFClient
    endpoint: str

    @pytest.fixture(autouse=True)
    def _setup(self, api: DRFClient) -> None:
        self.client = api
        self.endpoint = self.endpoint.removesuffix("/")


if TYPE_CHECKING:
    BaseTestT = BaseClientTest
else:
    BaseTestT = object


class PaginationTestMixin(BaseTestT):
    """Mixin for pagination tests."""

    pagination_factory_name: str

    pagination_request_params: Mapping = None  # type: ignore[assignment]
    empty_request_params: Mapping = None  # type: ignore[assignment]

    @pytest.fixture(autouse=True)
    def _setup_pagination_params(self) -> None:
        if self.pagination_request_params is None:
            self.pagination_request_params = {}  # type: ignore[unreachable]
        if self.empty_request_params is None:
            self.empty_request_params = {}  # type: ignore[unreachable]

    @pytest.fixture
    def items(self, request: FixtureRequest) -> list[T]:
        return cast(list["T"], request.getfixturevalue(self.pagination_factory_name))

    def test_pagination(self, items: list[T]) -> None:
        """Items pagination works correctly."""
        page_size = 3

        first_page = self.client.get(
            self.endpoint, data={"page[size]": page_size, **self.pagination_request_params})
        exact_page = self.client.get(
            self.endpoint, data={"page[size]": page_size, "page[number]": 2, **self.pagination_request_params})

        assert "links" in first_page
        assert len(first_page["data"]) == 3, (first_page, len(first_page["data"]))
        assert len(exact_page["data"]) > 0
        assert first_page["meta"]["pagination"]["count"] == settings.DEFAULT_SMALL_PAGE_SIZE + 1

    def test_empty_response(self) -> None:
        """If there are no items in the DB, an empty list is returned."""
        got = self.client.get(self.endpoint, params=self.empty_request_params)

        assert got["meta"]["pagination"]["count"] == 0
        assert len(got["data"]) == 0


class NotFoundTestMixin(BaseTestT):
    """Mixin for 'missing item' tests."""

    not_found_endpoint: str | None

    def get_not_found_endpoint(self, *args: Any, **kwargs: Any) -> str:
        if self.not_found_endpoint is not None:
            return self.not_found_endpoint
        return NotImplemented

    def test_not_found(self) -> None:
        """If the requested item is not found, response with a correct message and 404 status is returned."""
        got = self.client.get(self.get_not_found_endpoint(), expected_status_code=404)

        assert "error" in got
