"""Bookmark app model."""

# mypy: disable-error-code="var-annotated,attr-defined"
# ruff: noqa: ANN204
from django.contrib.auth import get_user_model
from django.db import models

from core.apps.articles.models import Article
from core.apps.general.models import TimestampedModel

User = get_user_model()


class ReadingCategory(TimestampedModel):
    """BookmarCategory."""

    title = models.CharField(max_length=60)
    description = models.TextField(blank=True)
    is_private = models.BooleanField(default=False)
    is_reading_list = models.BooleanField(default=False)
    bookmarks = models.ManyToManyField("Bookmark", through="BookmarksInCategories")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="bookmark_categories"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["title", "user"], name="unique_title_per_user"
            )
        ]
        verbose_name_plural = "ReadingCategories"

    def __str__(self):
        """Return User: {self.user.first_name} {self.user.last_name} user.Bookmark category{self.title}."""
        return f"User: {self.user.first_name} {self.user.last_name}'s Bookmark category: {self.title}."


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
        return f"Article: '{self.article.title}' bookmarked by user '{self.user.full_name}'"


class BookmarksInCategories(models.Model):
    """Bookmark & Reading Category through table."""

    category = models.ForeignKey(ReadingCategory, on_delete=models.CASCADE)
    bookmark = models.ForeignKey(
        Bookmark, on_delete=models.CASCADE, related_name="reading_categories"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["category", "bookmark"], name="unique_boomark_per_category"
            )
        ]
        verbose_name_plural = "BookmarksInCategories"

    def __str__(self):
        """Return Article: {self.bookmark.title} in user: {self.category.user.full_name}'s list: {self.category.title}."""
        return f"Article: {self.bookmark.article.title} in user: \
            {self.category.user.full_name}'s \
                list: {self.category.title}."


# TODO: Remove Bookmark model, using only ReadingCategory and Article to track bookmark
# TODO: Article doesn't need show bookmarked count and bookmarks
