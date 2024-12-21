"""Bookmark serializer."""

# ruff: noqa: ANN001
from rest_framework import serializers

from .models import Bookmark


class BookmarkSerializer(serializers.ModelSerializer):
    """Bookmark serializer."""

    article_info = serializers.SerializerMethodField()
    bookmarked_time = serializers.DateTimeField(
        source="created_at", format="%m/%d, %Y", read_only=True
    )

    class Meta:
        model = Bookmark
        fields = ["id", "article_info", "bookmarked_time"]

    def get_article_info(self, obj):
        """Return article's title, author, created time and image."""
        data = {}
        data["title"] = obj.article.title
        data["author"] = obj.article.author.full_name
        data["created_time"] = obj.article.created_at.strftime("%m/%d, %Y")
        try:
            data["banner_image"] = obj.article.banner_image.url
        except ValueError:
            data["banner_image"] = "No Image"
        return data
