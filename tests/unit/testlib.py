from __future__ import annotations

import json
import random
import string
from typing import TYPE_CHECKING, Any, cast

from model_bakery import baker
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from django.contrib.auth import get_user_model

if TYPE_CHECKING:
    from rest_framework.response import Response

    from django.contrib.auth.models import User as UserT

type APIResponse = dict[str, Any]

User = get_user_model()


class DRFClient(APIClient):
    """DRF API client for tests."""

    user: UserT | None = None
    god_mode: bool = False

    def __init__(
        self,
        user: UserT | None = None,
        god_mode: bool = True,
        anon: bool = False,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        if not anon:
            self.auth(user, god_mode)

    def auth(self, user: UserT | None = None, god_mode: bool = True) -> None:
        self.user = user or self._create_user(god_mode)
        self.god_mode = god_mode
        token = Token._default_manager.get_or_create(user=self.user)[0]
        self.credentials(
            HTTP_AUTHORIZATION=f"Bearer {token}",
        )

    def _create_user(self, god_mode: bool = True) -> UserT:
        user_opts = {}
        if god_mode:
            user_opts = {
                "is_staff": False,
                "is_superuser": True,
            }
        user = cast("UserT", baker.make(User, **user_opts))  # type: ignore[call-overload]
        self.password = "".join([random.choice(string.hexdigits) for _ in range(6)])
        user.set_password(self.password)
        user.save()
        return user

    def logout(self) -> None:
        self.credentials()
        super().logout()

    def get(self, *args: Any, **kwargs: Any) -> APIResponse:  # type: ignore[override]
        return self._api_call("get", kwargs.get("expected_status_code", 200), *args, **kwargs)

    def post(self, *args: Any, **kwargs: Any) -> APIResponse:  # type: ignore[override]
        return self._api_call("post", kwargs.get("expected_status_code", 201), *args, **kwargs)

    def put(self, *args: Any, **kwargs: Any) -> APIResponse:  # type: ignore[override]
        return self._api_call("put", kwargs.get("expected_status_code", 200), *args, **kwargs)

    def patch(self, *args: Any, **kwargs: Any) -> APIResponse:  # type: ignore[override]
        return self._api_call("patch", kwargs.get("expected_status_code", 200), *args, **kwargs)

    def delete(self, *args: Any, **kwargs: Any) -> APIResponse:  # type: ignore[override]
        return self._api_call("delete", kwargs.get("expected_status_code", 204), *args, **kwargs)

    def _api_call(self, method: str, expected: int, *args: Any, **kwargs: Any) -> APIResponse:
        kwargs["format"] = kwargs.get("format", "json")  # по умолчанию отравляем данные в json формате
        as_response = kwargs.pop("as_response", False)

        func = getattr(super(), method)
        response = func(*args, **kwargs)

        if as_response:
            return response  # type: ignore[no-any-return]

        content = self._decode(response)

        error_message = f"Got {response.status_code} instead of {expected}. Content is '{content}'"
        assert response.status_code == expected, error_message

        return content

    def _decode(self, response: Response) -> APIResponse:
        content = response.content.decode("utf-8", errors="ignore")
        if self.is_json(response):
            return cast(APIResponse, json.loads(content))
        return content  # type: ignore[no-any-return]

    @staticmethod
    def is_json(response: Response) -> bool:
        if response.has_header("content-type"):
            return "json" in response.get("content-type", "")
        return False
