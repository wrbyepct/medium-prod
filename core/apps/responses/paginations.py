"""Response custom paginations."""

from rest_framework.pagination import PageNumberPagination


class ResponsePagination(PageNumberPagination):
    """Response pagination class."""

    page_size = 10
    max_page_size = 20
    page_size_query_param = "page_size"
    page_query_param = "page"
