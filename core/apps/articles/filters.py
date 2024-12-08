"""Artice app filtes."""

import django_filters as filters

from .models import Article


class ArticleFilter(filters.FilterSet):
    """
    Custom artcile filter using fields.

    - author: author's first name (case-insensitive, contains)
    - title: article's title (case-insensitive, contains)
    - tags: article's tags (case-insensitive, exact match)
    - created_at: article created time
    - udpated_at: article updated time
    """

    author = filters.CharFilter(
        field_name="author__first_name",
        lookup_expr="icontains",
    )
    title = filters.CharFilter(field_name="title", lookup_expr="icontains")
    tags = filters.CharFilter(field_name="tags", lookup_expr="iexact")
    created_at = filters.DateFromToRangeFilter(field_name="created_at")
    updated_at = filters.DateFromToRangeFilter(field_name="updated_at")

    class Meta:
        model = Article
        fields = ["author", "title", "tags", "created_at", "updated_at"]
