"""Response serializers."""

from rest_framework import serializers

from .models import Response


class ResponseSerializer(serializers.ModelSerializer):
    """Response serializer."""

    user_name = serializers.SerializerMethodField()
    article_title = serializers.CharField(source="article.title", read_only=True)

    reply_to_response = serializers.PrimaryKeyRelatedField(
        queryset=Response.objects.all(), allow_null=True
    )

    def get_user_name(self, obj: Response):
        """Return user full name."""
        return obj.user.full_name

    class Meta:
        model = Response
        fields = [
            "id",
            "article_title",
            "user_name",
            "content",
            "claps_count",
            "replies_count",
            "reply_to_response",
        ]
        read_only_fields = ["replies_count", "claps_count"]
