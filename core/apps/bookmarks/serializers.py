"""Bookmark serializer."""

# ruff: noqa: ANN001

from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.apps.articles.models import Article

from .models import ReadingCategory

PARTIAL_ARITCLE_BODY_LENGTH = 134


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
        read_only_fields = ["title"]

    def get_partial_body(self, obj):
        """Return certain length of article's body."""
        text = obj.description + obj.body

        return (
            text[:PARTIAL_ARITCLE_BODY_LENGTH]
            if len(text) >= PARTIAL_ARITCLE_BODY_LENGTH
            else text
        )


class DynamicPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    """Cusom Primary key related field."""

    def get_queryset(self):
        """Filter results by requesting user."""
        return super().get_queryset().filter(user=self.context["request"].user)


class ReadingCategorySerializer(serializers.ModelSerializer):
    """ReadingCategory Serializer."""

    title = serializers.CharField(required=False)
    category = DynamicPrimaryKeyRelatedField(
        queryset=ReadingCategory.objects.all(),
        allow_null=True,
        required=False,
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
        """Allow only updating is_private and description for 'Reading list' category."""
        if instance.is_reading_list:
            validated_data.pop("title", None)
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
                instance.save()
            return instance

        return super().update(instance, validated_data)

    def create(self, validated_data):
        """
        Create a bookmark category or use an existing one.

        Add a bookmark if specified.

        """
        selected_category = validated_data.pop("category", None)

        if selected_category is None:
            title = validated_data.get("title", None)
            if title is None:
                detail = "Creating new category 'title' cannot be empty."
                raise ValidationError(detail=detail)

            validated_data["description"] = validated_data.get("description", "")
            validated_data["is_private"] = validated_data.get("is_private", False)

            bookmark_category = ReadingCategory.objects.create(**validated_data)

        else:
            bookmark_category = get_object_or_404(
                ReadingCategory, id=selected_category.id
            )

        article_id = self.context.get("article_id", None)
        if article_id:
            article = get_object_or_404(Article, id=article_id)
            bookmark_category.bookmarks.add(article)

        return bookmark_category

    def to_representation(self, instance):
        """Remove category from representation."""
        data = super().to_representation(instance)
        data.pop("category")
        return data
