"""Response serializers."""

from rest_framework import serializers

from .models import Response


class ResponseSerializer(serializers.ModelSerializer):
    """Response serializer."""

    user_name = serializers.SerializerMethodField()

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
        ]
        read_only_fields = ["replies_count", "claps_count", "article", "parent"]
