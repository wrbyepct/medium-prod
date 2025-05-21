"""Article model Manager."""

from django.db import models


class ArticleQuerySet(models.QuerySet):
    """Article custom queryset."""

    def join_author_table(self):
        """Join with author table."""
        return self.select_related("author")

    def with_response_and_claps_count(self):
        """Return with claps_count & responses_count fields."""
        return self.annotate(
            claps_count=models.Count("claps", distinct=True),
            responses_count=models.Count("responses", distinct=True),
        )

    def with_view_count_and_avg_rating(self):
        """Return with and average rating & views count fields."""
        return self.annotate(
            avg_rating=models.Avg("ratings"),
            views=models.Count("article_views", distinct=True),
        )

    def fetch_related(self):
        """
        Join table with author and then profile.

        fetch tags claps in resulting article ids.
        """
        return self.select_related("author__profile").prefetch_related(
            "tags", "claps__user"
        )


class ArticleManager(models.Manager):
    """Article manager."""

    def base_set(self):
        """Provide base set."""
        return ArticleQuerySet(model=self.model, using=self._db)

    def get_queryset(self):
        """Return optimized article queryset with pre-calculated fields."""
        return (
            self.base_set()
            .with_response_and_claps_count()
            .with_view_count_and_avg_rating()
            .fetch_related()
        )

    def preview_data(self):
        """
        Show preview article data.

        Field:
            "id"
            "title"
            "created_at"
            "banner_image"
            "author__first_name"
            "author__last_name"

        """
        return (
            self.base_set()
            .with_response_and_claps_count()
            .join_author_table()
            .only(
                "id",
                "title",
                "created_at",
                "banner_image",
                "body",
                "author__first_name",
                "author__last_name",
            )
            .order_by("-created_at")
        )

    def with_view_count_and_avg_rating(self):
        """Adding in avg: ratingg & count: view in fields."""
        return self.base_set().with_view_count_and_avg_rating()
