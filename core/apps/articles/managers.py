"""Article model Manager."""

from django.db import models
from django.db.models import OuterRef, Subquery
from django.db.models.functions import Coalesce


class ArticleQuerySet(models.QuerySet):
    """Article custom queryset."""

    def join_author_table(self):
        """Join with author table."""
        return self.select_related("author")

    def with_response_and_claps_count(self):
        """Return with claps_count & responses_count fields."""
        from core.apps.responses.models import Response

        from .models import Clap

        # Use subquery to calculate in a nested query to avoid table joining
        claps_count_subquery = (
            Clap.objects.filter(article=OuterRef("pk"))
            .order_by()
            .values("article")
            .annotate(claps_count=models.Count("id"))
            .values("claps_count")
        )

        responses_count_subquery = (
            Response.objects.filter(article=OuterRef("pk"))
            .order_by()
            .values("article")
            .annotate(responses_count=models.Count("id"))
            .values("responses_count")
        )
        return self.annotate(
            claps_count=Coalesce(
                Subquery(claps_count_subquery),
                0,
            ),
            responses_count=Coalesce(
                Subquery(responses_count_subquery),
                0,
            ),
        )

    def with_view_count_and_avg_rating(self):
        """Return with and average rating & views count fields."""
        from core.apps.articles.models import ArticleView
        from core.apps.ratings.models import Rating

        # Use subquery to calculate in a nested query to avoid table joining
        avg_rating_subquery = (
            Rating.objects.filter(article=OuterRef("pk"))
            .order_by()
            .values("article")
            .annotate(avg_rating=models.Avg("rating"))
            .values("avg_rating")
        )

        views_count_subquery = (
            ArticleView.objects.filter(article=OuterRef("pk"))
            .order_by()
            .values("article")
            .annotate(views_count=models.Count("id"))
            .values("views_count")
        )
        return self.annotate(
            avg_rating=Coalesce(
                Subquery(avg_rating_subquery),
                0.0,
            ),
            views=Coalesce(
                Subquery(views_count_subquery),
                0,
            ),
        )

    def fetch_related(self):
        """
        Join table with author and then profile.

        fetch tags claps in resulting article ids.
        """
        # TODO consider dedicate tags and claps user info to claps retrieval
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
