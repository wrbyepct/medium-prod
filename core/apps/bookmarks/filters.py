"""Bookmark filters."""

import django_filters as filters

from .models import Bookmark


class BookmarkFilter(filters.FilterSet):
    """Custom Bookmark filter."""

    title = filters.CharFilter(field_name="article__title", lookup_expr="icontains")
    author_name = filters.CharFilter(
        field_name="article__author__first_name", lookup_expr="icontains"
    )
    bookmarked_time = filters.DateFromToRangeFilter(field_name="created_at")
    article_created_time = filters.DateFromToRangeFilter(
        field_name="article__created_at"
    )

    class Meta:
        model = Bookmark
        fields = ["title", "author_name", "bookmarked_time", "article_created_time"]
