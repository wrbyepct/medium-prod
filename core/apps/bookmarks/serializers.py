"""Bookmark serializer."""

# ruff: noqa: ANN001

from django.shortcuts import get_object_or_404
from rest_framework import serializers

from core.apps.articles.models import Article
from core.apps.articles.serializers import ArticlePreviewSerializer

from .models import ReadingCategory


class BookmarkSerializer(ArticlePreviewSerializer):
    """Bookmark Serializer."""


class DynamicPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    """Cusom Primary key related field."""

    def get_queryset(self):
        """Filter results by requesting user."""
        return super().get_queryset().filter(user=self.context["request"].user)


class ReadingCategorySerializer(serializers.ModelSerializer):
    """ReadingCategory Serializer."""

    category = DynamicPrimaryKeyRelatedField(
        queryset=ReadingCategory.objects.all(),
        allow_null=True,
        required=False,
        write_only=True,
    )

    bookmarks = BookmarkSerializer(many=True, read_only=True)
    bookmarks_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = ReadingCategory
        fields = [
            "id",
            "slug",
            "title",
            "description",
            "is_private",
            "category",
            "updated_at",
            "bookmarks_count",
            "bookmarks",
        ]
        read_only_fields = ["id", "slug"]

    def update(self, instance, validated_data):
        """Cannot update default 'Reading list' category's title."""
        if instance.is_reading_list:
            validated_data.pop("title", None)
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
                instance.save()
            return instance

        return super().update(instance, validated_data)

    def handle_article_adding(self, bookmark_category):
        """Add article to the category if specifed."""
        article_id = self.context.get("article_id", None)

        if article_id:
            article = get_object_or_404(Article, id=article_id)
            bookmark_category.bookmarks.add(article)

    def create(self, validated_data):
        """
        Create a bookmark category or use an existing one.

        Add a bookmark if specified.
        """
        bookmark_category = super().create(validated_data)
        self.handle_article_adding(bookmark_category)
        return bookmark_category
