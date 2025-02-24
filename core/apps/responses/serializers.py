"""Response serializers."""

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Response


class ResponseSerializer(serializers.ModelSerializer):
    """Response serializer."""

    user_full_name = serializers.SerializerMethodField()
    claps_count = serializers.IntegerField(read_only=True)
    replies_count = serializers.IntegerField(read_only=True)
    article_id = serializers.SerializerMethodField()
    parent_id = serializers.SerializerMethodField()

    def get_article_id(self, obj: Response):
        """Return response aritcle id."""
        return obj.article.id

    def get_parent_id(self, obj: Response):
        """Return response aritcle id."""
        return obj.parent.id if obj.parent else None

    def get_user_full_name(self, obj: Response):
        """Return user full name."""
        return obj.user.full_name

    def validate_content(self, value: str):
        """Raise Validation Error if content provided is empty."""
        value.strip()
        if not value:
            detail = "Response content cannot be empty."
            raise ValidationError(detail=detail)
        return value

    class Meta:
        model = Response
        fields = [
            "id",
            "user_full_name",
            "content",
            "article_id",
            "parent_id",
            "claps_count",
            "replies_count",
            "created_at",
        ]
        read_only_fields = [
            "created_at",
        ]
