from __future__ import annotations

from typing import TYPE_CHECKING

from rest_framework.response import Response
from rest_framework.views import APIView

if TYPE_CHECKING:
    from rest_framework.request import Request


class Healthcheck(APIView):
    """Проверка состояния сервиса."""

    authentication_classes = []
    permission_classes = []

    def get(self, _: Request) -> Response:
        """Проверка состояния сервиса."""
        return Response({"status": "ok"})
