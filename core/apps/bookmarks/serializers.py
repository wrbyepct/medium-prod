"""Bookmark serializer."""

# ruff: noqa: ANN001

from django.shortcuts import get_object_or_404
from rest_framework import serializers

from core.apps.articles.models import Article
from core.apps.articles.serializers import ArticlePreviewSerializer

from .constants import MAX_TITLE_LENGTH
from .exceptions import TitleEmptyError, TitleTooLongError
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

    title = serializers.CharField(required=False)

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

    def validate_title(self, value):
        """Validate too long."""
        if len(value) > MAX_TITLE_LENGTH:
            raise TitleTooLongError
        return value

    def create(self, validated_data):
        """
        Create a bookmark category or use an existing one.

        Add a bookmark if specified.
        """
        category = validated_data.pop("category", None)
        if not category:
            category = self.hande_create_new_category(validated_data)
        self.handle_article_adding(category)
        return category

    def handle_article_adding(self, bookmark_category):
        """Add article to the category if specifed."""
        article_id = self.context.get("article_id", None)

        if article_id:
            article = get_object_or_404(Article, id=article_id)
            bookmark_category.bookmarks.add(article)

    def hande_create_new_category(self, validated_data):
        """
        Handle create new category.

        Raise error if title is empty.
        """
        if not validated_data.get("title", None):
            raise TitleEmptyError
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """Update category's data."""
        if instance.is_reading_list:
            return self.handle_updating_default_category(
                validated_data=validated_data, instance=instance
            )
        return super().update(instance, validated_data)

    def handle_updating_default_category(self, validated_data, instance):
        """Handle cannot update default 'Reading list' category's title.."""
        validated_data.pop("title", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            instance.save()
        return instance
