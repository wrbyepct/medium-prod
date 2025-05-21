"""Response Model Manager."""

from django.db import models


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
            .order_by("-created_at")
        )
