"""Rating serializers."""

from rest_framework import serializers

from .models import Rating


class RatingSerializer(serializers.ModelSerializer):
    """Rating serializer."""

    article_title = serializers.CharField(source="article.title", read_only=True)
    user_full_name = serializers.CharField(source="user.first_name", read_only=True)

    class Meta:
        model = Rating
        fields = ["id", "article_title", "user_full_name", "rating", "review"]

    def get_user_full_name(self, obj: Rating):
        """Return user's full name."""
        return obj.user.full_name
