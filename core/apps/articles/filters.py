"""Artice app filtes."""

import django_filters as filters

from .models import Article


class ArticleFilter(filters.FilterSet):
    """
    Custom artcile filter using fields.

    - tags: article's tags name (case-insensitive, exact match)
    - created_at: article created time
    - udpated_at: article updated time
    """

    tags = filters.CharFilter(field_name="tags__name", lookup_expr="iexact")
    created_at = filters.DateFromToRangeFilter(field_name="created_at")
    updated_at = filters.DateFromToRangeFilter(field_name="updated_at")

    class Meta:
        model = Article
        fields = ["tags", "created_at", "updated_at"]
