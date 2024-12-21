"""Bookmark app model."""

# mypy: disable-error-code="var-annotated,attr-defined"
# ruff: noqa: ANN204
from django.contrib.auth import get_user_model
from django.db import models

from core.apps.articles.models import Article
from core.apps.general.models import TimestampedModel

User = get_user_model()


class Bookmark(TimestampedModel):
    """Bookmark model."""

    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="bookmarks"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookmarks")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["article", "user"],
                name="unique_user_bookmark_per_article",
            )
        ]
        ordering = ["-created_at"]

    def __str__(self):
        """Return string name Article: '{self.article.title}' bookmarked by user '{self.user.first_name}'."""
        return f"Article: '{self.article.title}' bookmarked by user '{self.user.first_name}'"
