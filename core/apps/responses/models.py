"""Responses models."""

# mypy: disable-error-code="var-annotated"
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.apps.articles.models import Article
from core.apps.general.models import TimestampedModel

User = get_user_model()


class ResponseManager(models.Manager):
    """Response Manager."""

    def get_queryset(self):
        """
        Return optimized queryset.

        Select on FK: article, user, parent.
        Only with Columns:
           - id, content,
           - claps_count,
           - replies_count,
           - created_at,
           - user_name,
           - article_id,
           - parent_id
        """
        return (
            super()
            .get_queryset()
            .select_related("article", "user", "parent")
            .only(
                "id",
                "content",
                "claps_count",
                "replies_count",
                "created_at",
                "user__first_name",
                "user__last_name",
                "article__id",
                "parent__id",
            )
        )


class ResponseClap(TimestampedModel):
    """Respone clap model."""

    response = models.ForeignKey(
        "Response", on_delete=models.CASCADE, related_name="claps"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["response", "user"],
                name="unique_clap_per_response_for_one_user",
            )
        ]

    def __str__(self) -> str:
        """Return User: {self.user.full_name} clapped the response by {self.response.user.full_name}."""
        return f"User: {self.user.full_name} clapped the response by {self.response.user.full_name}."


class Response(TimestampedModel):
    """Response model."""

    content = models.TextField(blank=True, verbose_name=_("response content"))
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="responses"
    )
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )
    replies_count = models.PositiveSmallIntegerField(default=0)
    claps_count = models.PositiveSmallIntegerField(default=0)

    objects = ResponseManager()

    class Meta:
        ordering = ["-claps_count"]
        indexes = [
            models.Index(fields=["claps_count", "created_at", "updated_at"]),
            models.Index(fields=["article_id", "parent_id"]),
            models.Index(fields=["parent_id"]),
        ]

    def __str__(self) -> str:
        """User: {self.user.full_name}'s response to article: {self.article.title}."""
        return (
            f"User: {self.user.full_name}'s response to article: {self.article.title}"
        )


# Create your models here.
