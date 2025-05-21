"""Ratings models."""

# mypy: disable-error-code="var-annotated"
from django.contrib.auth import get_user_model
from django.db import models

from core.apps.articles.models import Article
from core.apps.general.models import TimestampedModel

from .managers import RatingManager

User = get_user_model()


class Rating(TimestampedModel):
    """Rating Model."""

    RATING_CHOICES = [
        (1, "Poor"),
        (2, "Fair"),
        (3, "Good"),
        (4, "Very Good"),
        (5, "Exellent"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="ratings",
    )
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    review = models.TextField(blank=True)

    objects = RatingManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["article", "user"],
                name="unqiue_rating_per_article_and_user",
            ),
        ]

    def __str__(self) -> str:
        """Return Article:{self.aritcle.titel} rated: {self.rating} by user: {self.user.full_name}."""
        return f"Article:{self.article.title} rated: {self.rating} by user: {self.user.full_name}"
