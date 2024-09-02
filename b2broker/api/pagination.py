from rest_framework_json_api.pagination import JsonApiPageNumberPagination

from django.conf import settings


class SmallResultsSetPagination(JsonApiPageNumberPagination):  # type: ignore[misc]
    page_size = settings.DEFAULT_SMALL_PAGE_SIZE
