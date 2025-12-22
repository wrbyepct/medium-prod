"""Article app serializer."""

# ruff: noqa: ANN001
from __future__ import annotations

import json
import logging

from rest_framework import serializers

from core.apps.profiles.serializers import ProfileSerializer

from .models import Article, Clap

logger = logging.getLogger(__name__)


class ClapSerializer(serializers.ModelSerializer):
    """Clap serializer."""

    user_name = serializers.SerializerMethodField()

    created_at = serializers.DateTimeField(format="%m/%d/%Y, %H:%M:%S", read_only=True)

    def get_user_name(self, obj):
        """Return user full name."""
        return obj.user.full_name

    class Meta:
        model = Clap
        fields = ["user_name", "created_at"]


class TagListField(serializers.Field):
    """Tag List field."""

    def to_representation(self, value):
        """Represent the data as the list of string tag name."""
        return [tag.name for tag in value.all()]

    def check_data_type(self, data):
        """
        Raise TypeError if input data cannot be converted to list of string elements.

        Otherwise it returns the converted value.
        """
        data_list = json.loads(data)

        if not isinstance(data_list, list) or not all(
            isinstance(item, str) for item in data_list
        ):
            raise ValueError
        return data_list

    def to_internal_value(self, data: str) -> list[str]:
        """
        Filter out empty string and return a list of string.

        Raises
          - serializer.ValidationError: If input data cannot be converted to list object of string elements.

        """
        error_detail = (
            """Expected a string of list of tags.\n E.g., '["tag1", "tag2"]'"""
        )

        try:
            data_list = self.check_data_type(data)

        except (ValueError, TypeError) as invalid_tags_format:
            raise serializers.ValidationError(
                detail=error_detail
            ) from invalid_tags_format

        return [tag.strip() for tag in data_list if tag.strip()]


PARTIAL_ARITCLE_BODY_MAX_LENGTH = 134


class ArticlePreviewSerializer(serializers.ModelSerializer):
    """Article preview Serializer."""

    author_fullname = serializers.SerializerMethodField()
    claps_count = serializers.IntegerField(read_only=True)
    responses_count = serializers.IntegerField(read_only=True)
    partial_body = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%b %d, %Y", read_only=True)

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "author_fullname",
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

    def get_author_fullname(self, obj):
        """Return author's full name."""
        return obj.author.full_name

    def get_partial_body(self, obj):
        """Return certain length of article's body."""
        return self._handle_text_length(obj.description + obj.body)


class ArticleSerializer(serializers.ModelSerializer):
    """Article Serializer."""

    responses_count = serializers.IntegerField(read_only=True)
    clapped_by = ClapSerializer(source="claps", many=True, read_only=True)
    claps_count = serializers.IntegerField(read_only=True)

    views = serializers.IntegerField(read_only=True)
    avg_rating = serializers.DecimalField(
        max_digits=3, decimal_places=2, coerce_to_string=False, read_only=True
    )
    author_info = ProfileSerializer(source="author.profile", read_only=True)
    created_at = serializers.DateTimeField(format="%m/%d/%Y, %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%m/%d/%Y, %H:%M:%S", read_only=True)

    tags = TagListField(required=False)

    def to_representation(self, instance: Article):
        """Return article's banner image relative urls instead of absolute one."""
        data = super().to_representation(instance)

        data["banner_image"] = (
            getattr(instance.banner_image, "url", "No image")
            if instance.banner_image
            else "No image"
        )

        return data

    def update(self, instance: Article, validated_data):
        """User can only update 'title', 'body', 'description', 'banner_image', 'updated_time'."""
        instance.title = validated_data.get("title", instance.title)
        instance.body = validated_data.get("body", instance.body)
        instance.banner_image = validated_data.get(
            "banner_image",
            instance.banner_image,
        )
        instance.description = validated_data.get("description", instance.description)
        instance.updated_at = validated_data.get("updated_at", instance.updated_at)

        tags = validated_data.pop("tags", None)
        if tags is not None:
            instance.tags.set(tags)

        instance.save()
        return instance

    def create(self, validated_data):
        """Create Article instance and set tags for it."""
        tags = validated_data.pop("tags", None)
        article = Article.objects.create(**validated_data)
        if tags is not None:
            article.tags.set(tags)

        return article

    class Meta:
        model = Article
        fields = [
            "id",
            "slug",
            "title",
            "description",
            "banner_image",  # return relative url
            "body",
            "tags",
            "estimated_reading_time",  # property: read-only
            "avg_rating",  # property: read-only
            "views",  # property: read-only
            "responses_count",  # read-only
            "claps_count",  #  read-only
            "clapped_by",  # read-only
            "created_at",  # serializer method: read-only
            "updated_at",  # serializer method: read-only
            "author_info",  # nested info: read-only
        ]
        read_only_fields = ["slug"]
