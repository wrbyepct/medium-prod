"""Pagination class."""

from rest_framework.pagination import PageNumberPagination


class ArticlePagination(PageNumberPagination):
    """Custom pagination class."""

    page_size = 10
    max_page_size = 20
    page_query_param = "page"
    page_size_query_param = "page_size"
