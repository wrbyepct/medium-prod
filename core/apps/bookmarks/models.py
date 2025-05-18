"""Bookmark app model."""

# mypy: disable-error-code="var-annotated,attr-defined"
# ruff: noqa: ANN204

from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.db import models

from core.apps.articles.models import Article
from core.apps.general.models import TimestampedModel
from core.tools.hash import generate_hashed_slug

from .constants import MAX_TITLE_LENGTH

User = get_user_model()


class ReadingCategoryManager(models.Manager):
    """ReadingCategory manager."""

    def get_queryset(self):
        """Return queryset with annotated field: boomarks_count. Prefetch bookmarks."""
        return (
            super()
            .get_queryset()
            .annotate(bookmarks_count=models.Count("bookmarks", distinct=True))
            .prefetch_related(
                models.Prefetch(
                    "bookmarks", queryset=Article.statistic_objects.preview_data()
                ),
            )
            .order_by("-is_reading_list", "-created_at")
        )


class ReadingCategory(TimestampedModel):
    """BookmarCategory."""

    title = models.CharField(
        validators=[MinLengthValidator(1)], max_length=MAX_TITLE_LENGTH
    )
    slug = AutoSlugField(
        populate_from=generate_hashed_slug, always_update=True, unique=True
    )
    description = models.TextField(blank=True)
    is_private = models.BooleanField(default=False)
    is_reading_list = models.BooleanField(default=False)
    bookmarks = models.ManyToManyField(Article, through="BookmarksInCategories")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reading_categories"
    )

    objects = ReadingCategoryManager()

    class Meta:
        ordering = ["-is_reading_list"]
        verbose_name_plural = "ReadingCategories"

    def __str__(self):
        """Return User: {self.user.first_name} {self.user.last_name} user.Bookmark category{self.title}."""
        return f"User: {self.user.first_name} {self.user.last_name}'s Bookmark category: {self.title}."


class BookmarksInCategories(models.Model):
    """Bookmark & Reading Category through table."""

    category = models.ForeignKey(ReadingCategory, on_delete=models.CASCADE)
    bookmark = models.ForeignKey(Article, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["category", "bookmark"], name="unique_boomark_per_category"
            )
        ]

        verbose_name_plural = "BookmarksInCategories"

    def __str__(self):
        """Return Article: {self.bookmark.title} in user: {self.category.user.full_name}'s list: {self.category.title}."""
        return f"Article: {self.bookmark.title} in user: {self.category.user.full_name}'s list: {self.category.title}."
