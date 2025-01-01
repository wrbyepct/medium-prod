"""Bookmark serializer."""

# ruff: noqa: ANN001

from django.shortcuts import get_object_or_404
from rest_framework import serializers

from core.apps.articles.models import Article

from .models import ReadingCategory

PARTIAL_ARITCLE_BODY_LENGTH = 134


class BookmarkSerializer(serializers.ModelSerializer):
    """Bookmark Serializer."""

    partial_body = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%b %d, %Y")
    claps_count = serializers.SerializerMethodField()
    responses_count = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "partial_body",
            "banner_image",
            "created_at",
            "claps_count",
            "responses_count",
        ]
        read_only_fields = ["title", "created_at"]

    def get_claps_count(self, obj):
        """Return all claps count."""
        return obj.claps.all().count()

    def get_responses_count(self, obj):
        """Return all responsess count."""
        return obj.responses.all().count()

    def get_partial_body(self, obj):
        """Return certain length of article's body."""
        text = obj.description + obj.body

        return (
            text[:PARTIAL_ARITCLE_BODY_LENGTH]
            if len(text) >= PARTIAL_ARITCLE_BODY_LENGTH
            else text
        )


class ReadingCategorySerializer(serializers.ModelSerializer):
    """ReadingCategory Serializer."""

    bookmarks = BookmarkSerializer(many=True, read_only=True)
    bookmarks_count = serializers.SerializerMethodField()
    title = serializers.CharField(required=False)

    class Meta:
        model = ReadingCategory
        fields = [
            "id",
            "slug",
            "title",
            "description",
            "is_private",
            "bookmarks_count",
            "bookmarks",
        ]
        read_only_fields = ["id", "slug"]

    def get_bookmarks_count(self, obj):
        """Return boomarks count."""
        return obj.bookmarks.all().count()

    def update(self, instance, validated_data):
        """Allow only updating is_private and description for 'Reading list' category."""
        if instance.is_reading_list:
            validated_data.pop("title", None)
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
                instance.save()
            return instance

        return super().update(instance, validated_data)

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
