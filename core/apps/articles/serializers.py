"""Article app serializer."""

# ruff: noqa: ANN001
from __future__ import annotations

import json
import logging

from rest_framework import serializers

from core.apps.profiles.serializers import ProfileSerializer

from .models import Article

logger = logging.getLogger(__name__)


class TagListField(serializers.Field):
    """Tag List field."""

    def to_representation(self, value):
        """Represent the data as the list of string tag name."""
        return [tag.name for tag in value.all()]

    def to_internal_value(self, data: str):
        """Filter out empty string and return a list of string."""
        try:
            data_list = json.loads(data)

        except ValueError as invalid_tags_format:
            detail = """Expected a string of list of tags.\n E.g., '["tag1", "tag2"]'"""
            raise serializers.ValidationError(detail=detail) from invalid_tags_format

        tags = []

        for tag in data_list:
            tag_name = tag.strip()
            if not tag_name:  # This allows user to accidentally add empty tag name. we just need to ignore it.
                continue

            tags.append(tag_name)
        return tags


class ArticleSerializer(serializers.ModelSerializer):
    """Article Serializer."""

    author_info = ProfileSerializer(source="author.profile", read_only=True)
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    tags = TagListField()

    def get_created_at(self, obj: Article) -> str:
        """
        Return formatted time: '%m/%d/%Y, %H:%M:%S'.

        Args:
            obj (Article): Article instance.

        Returns:
            str: formatted time: "%m/%d/%Y, %H:%M:%S"

        """
        return obj.created_at.strftime("%m/%d/%Y, %H:%M:%S")

    def get_updated_at(self, obj: Article) -> str:
        """
        Return formatted time: '%m/%d/%Y, %H:%M:%S'.

        Args:
            obj (Article): Article instance.

        Returns:
            str: formatted time: "%m/%d/%Y, %H:%M:%S"

        """
        return obj.updated_at.strftime("%m/%d/%Y, %H:%M:%S")

    def to_representation(self, instance: Article):
        """Return article's banner image relative urls instead of absolute one."""
        data = super().to_representation(instance)
        try:
            data["banner_image"] = instance.banner_image.url
        except ValueError:
            data["banner_image"] = "No image"

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
            "body",
            "tags",
            "estimated_reading_time",  # property: read-only
            "views",  # property: read-only
            "average_rating",  # property: read-only
            "banner_image",  # return relative url
            "created_at",  # serializer method: read-only
            "updated_at",  # serializer method: read-only
            "author_info",  # nested info: read-only
        ]
