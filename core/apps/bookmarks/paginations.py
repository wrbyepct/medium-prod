"""Bookmark pagination class."""

from rest_framework.pagination import PageNumberPagination


class BookmarkPagination(PageNumberPagination):
    """Custom pagination class."""

    page_size = 15
    page_query_param = "page_size"
    max_page_size = 30
