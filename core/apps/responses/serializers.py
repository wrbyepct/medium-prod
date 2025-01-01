"""Response serializers."""

from rest_framework import serializers

from .models import Response


class ResponseSerializer(serializers.ModelSerializer):
    """Response serializer."""

    user_name = serializers.SerializerMethodField()
    claps_count = serializers.IntegerField(read_only=True)
    replies_count = serializers.IntegerField(read_only=True)

    def get_user_name(self, obj: Response):
        """Return user full name."""
        return obj.user.full_name

    class Meta:
        model = Response
        fields = [
            "id",
            "user_name",
            "content",
            "article",
            "parent",
            "claps_count",
            "replies_count",
            "created_at",
        ]
        read_only_fields = [
            "article",
            "parent",
            "created_at",
        ]
