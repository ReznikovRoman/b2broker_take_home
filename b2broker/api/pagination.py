from rest_framework_json_api.pagination import PageNumberPagination


class SmallResultsSetPagination(PageNumberPagination):  # type: ignore[misc]
    page_size = 10
