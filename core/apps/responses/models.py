"""Responses models."""

# mypy: disable-error-code="var-annotated"
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.apps.articles.models import Article
from core.apps.general.models import TimestampedModel

User = get_user_model()


class ResponseQuerySet(models.QuerySet):
    """
    Custom ResponseQuerySet class.

    Methods
        join_user_table()
        with_count_data()
        with_necessary_colums_only()

    """

    def join_user_table(self):
        """Join with user table by select_related('user')."""
        return self.select_related("user")

    def with_count_data(self):
        """Annoate claps_count and replies_count columns."""
        return self.annotate(
            claps_count=models.Count("claps", distinct=True),
            replies_count=models.Count("children", distinct=True),
        )

    def with_necessary_colums_only(self):
        """
        Return queryset by selecting only the necessary columns.

        Columns:
            "id",
            "content",
            "created_at",
            "user__first_name",
            "user__last_name",
            "article_id",
            "parent_id",
        """
        return self.only(
            "id",
            "content",
            "created_at",
            "user__first_name",
            "user__last_name",
            "article_id",
            "parent_id",
        )


class ResponseManager(models.Manager):
    """Response Manager."""

    def get_queryset(self):
        """
        Use custom ResponseQuerySet class.

        Return all response instances.
        """
        return ResponseQuerySet(model=self.model, using=self._db)

    def default_data(self):
        """
        Return optimized queryset.

        Select related on FK: user
        Only with Columns:
           - id,
           - content,
           - claps_count, (annotated)
           - replies_count, (annotated)
           - created_at,
           - user_first_name,
           - user_last_name,
           - article_id,
           - parent_id
        """
        return (
            self.get_queryset()
            .with_necessary_colums_only()
            .with_count_data()
            .join_user_table()
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
        "self",
        on_delete=models.CASCADE,
        related_name="children",
        null=True,
        blank=True,
    )

    objects = ResponseManager()

    def __str__(self) -> str:
        """User: {self.user.full_name}'s response to article: {self.article.title}."""
        return (
            f"User: {self.user.full_name}'s response to article: {self.article.title}"
        )
