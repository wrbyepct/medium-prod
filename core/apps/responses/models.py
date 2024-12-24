"""Responses models."""

# mypy: disable-error-code="var-annotated"
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey

from core.apps.articles.models import Article
from core.apps.general.models import TimestampedModel

User = get_user_model()


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


class Response(TimestampedModel, MPTTModel):
    """Response model."""

    content = models.TextField(blank=True, verbose_name=_("response content"))
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="responses"
    )
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )

    class Meta:
        ordering = ["created_at"]

    def __str__(self) -> str:
        """User: {self.user.full_name}'s response to article: {self.article.title}."""
        return (
            f"User: {self.user.full_name}'s response to article: {self.article.title}"
        )


# Create your models here.
