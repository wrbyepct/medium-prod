"""Bookmark serializer."""

# ruff: noqa: ANN001

from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.apps.articles.models import Article

from .models import ReadingCategory

PARTIAL_ARITCLE_BODY_MAX_LENGTH = 134


class BookmarkSerializer(serializers.ModelSerializer):
    """Bookmark Serializer."""

    claps_count = serializers.IntegerField(read_only=True)
    responses_count = serializers.IntegerField(read_only=True)
    partial_body = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%b %d, %Y", read_only=True)

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
        read_only_fields = ["title", "banner_image"]

    def _handle_text_length(self, text):
        return (
            text[:PARTIAL_ARITCLE_BODY_MAX_LENGTH]
            if len(text) >= PARTIAL_ARITCLE_BODY_MAX_LENGTH
            else text
        )

    def get_partial_body(self, obj):
        """Return certain length of article's body."""
        return self._handle_text_length(obj.description + obj.body)


class DynamicPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    """Cusom Primary key related field."""

    def get_queryset(self):
        """Filter results by requesting user."""
        return super().get_queryset().filter(user=self.context["request"].user)


class ReadingCategorySerializer(serializers.ModelSerializer):
    """ReadingCategory Serializer."""

    title = serializers.CharField(
        required=False
    )  # if existing category is selected, this field is not required
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

    def get_or_create_category(self, validated_data):
        """
        Get or create ReadingCategory instance.

        Raise ValidationError if 'title' is not provided.

        """
        selected_category = validated_data.pop("category", None)
        if selected_category is None:
            title = validated_data.get("title", None)
            if title is None:
                detail = "Creating new category 'title' cannot be empty."
                raise ValidationError(detail=detail)

            validated_data["description"] = validated_data.get("description", "")
            validated_data["is_private"] = validated_data.get("is_private", False)

            return ReadingCategory.objects.create(**validated_data)

        return get_object_or_404(
            ReadingCategory, id=selected_category.id, user=validated_data["user"]
        )

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
        bookmark_category = self.get_or_create_category(validated_data)
        self.handle_article_adding(bookmark_category)
        return bookmark_category
