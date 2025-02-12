"""Custom Rating pagination."""

from rest_framework.pagination import PageNumberPagination


class RatingPagination(PageNumberPagination):
    """Custome rating pagination."""

    page_size = 15
    page_query_param = "page"
    page_size_query_param = "page_size"
    max_page_size = 25
