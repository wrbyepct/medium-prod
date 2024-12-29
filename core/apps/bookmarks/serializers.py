"""Bookmark serializer."""

# ruff: noqa: ANN001

from django.shortcuts import get_object_or_404
from rest_framework import serializers

from core.apps.articles.models import Article

from .models import ReadingCategory

# # TODO: Think about how to Re-implement Bookmark serialzier


class ReadingCategorySerializer(serializers.ModelSerializer):
    """ReadingCategory Serializer."""

    title = serializers.CharField(required=False)

    class Meta:
        model = ReadingCategory
        fields = ["id", "title", "description", "is_private"]

    def create(self, validated_data):
        """Get or create a bookmark categoyr and associate it with an article."""
        # Check to-boomark article existence
        article_id = self.context.get("article_id", None)
        article = get_object_or_404(Article, id=article_id)

        # Try to get exisitng category or create a new category
        title = validated_data.get("title", "Reading list")  # Default to "Reading list"
        user = validated_data.get("user")
        bookmark_category, _ = ReadingCategory.objects.get_or_create(
            user=user,
            title=title,
            defaults={
                "description": validated_data.get("description", ""),
                "is_private": validated_data.get("is_private", False),
            },
        )

        bookmark_category.bookmarks.add(article)

        return bookmark_category
