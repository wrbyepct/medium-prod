"""Bookmark serializer."""

# ruff: noqa: ANN001

from django.shortcuts import get_object_or_404
from rest_framework import serializers

from core.apps.articles.models import Article

from .models import ReadingCategory

# # TODO: Think about how to Re-implement Bookmark serialzier


class BookmarkSerializer(serializers.ModelSerializer):
    """Bookmark Serializer."""

    created_at = serializers.DateTimeField(format="%m, %d, %Y")
    partial_body = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "partial_body",
            "created_at",
            "claps_count",
            "responses_count",
        ]
        read_only_fields = ["title", "created_at", "claps_count", "responses_count"]

    def get_partial_body(self, obj):
        """Return certain length of article's body."""
        text = obj.description + obj.body
        display_length = 133
        return text[:134] if len(text) > display_length else text


class ReadingCategorySerializer(serializers.ModelSerializer):
    """ReadingCategory Serializer."""

    title = serializers.CharField(required=False)

    class Meta:
        model = ReadingCategory
        fields = ["id", "title", "description", "bookmarks_count", "is_private"]
        read_only_fields = ["id", "bookmarks_count"]

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
