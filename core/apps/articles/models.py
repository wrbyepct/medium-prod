"""Article app model."""

# mypy: disable-error-code="var-annotated,attr-defined"
# ruff: noqa: D105
from __future__ import annotations

from typing import TYPE_CHECKING

from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager

from core.apps.general.models import TimestampedModel
from core.tools.hash import generate_hashed_slug

from .services.read_time_engine import ArticleReadTimeEngine

if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractBaseUser

User = get_user_model()


class Clap(TimestampedModel):
    """Artitcle claps model."""

    article = models.ForeignKey(
        "Article", on_delete=models.CASCADE, related_name="claps"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["article", "user"], name="unique_article_per_user"
            )
        ]
        ordering = ["-created_at"]

    def __str__(self) -> str:
        """Return "User: {self.user.first_name} clapped the article: {self.article.title}"."""
        return f"User: {self.user.first_name} clapped the article: {self.article.title}"


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
                "author__first_name",
                "author__last_name",
            )
        )

    def with_view_count_and_avg_rating(self):
        """Adding in avg: ratingg & count: view in fields."""
        return self.base_set().with_view_count_and_avg_rating()


# Create your models here.
class Article(TimestampedModel):
    """Article mode."""

    title = models.CharField(verbose_name=_("Title"), max_length=255)
    description = models.CharField(
        verbose_name=_("Description"),
        max_length=255,
        blank=True,
    )
    body = models.TextField(verbose_name=_("article content"))
    banner_image = models.ImageField(
        verbose_name=_("Banner Image"),
        null=True,
        blank=True,
    )
    slug = AutoSlugField(
        populate_from=generate_hashed_slug,
        always_update=True,
        unique=True,
        max_length=300,  # default is 50
    )

    author = models.ForeignKey(User, related_name="articles", on_delete=models.CASCADE)
    tags = TaggableManager()
    statistic_objects = ArticleManager()
    objects = models.Manager()

    @property
    def user(self):
        """Return also user, for accessing convenience."""
        return self.author

    @cached_property
    def estimated_reading_time(self):
        """Return estimated article reading time."""
        return ArticleReadTimeEngine.get_reading_time(article=self)

    def __str__(self) -> str:
        return f"{self.author}'s article | {self.title}"

    def check_invalidate_cached_read_time(self):
        """Invalidated cached read time when updating and columns involving word count changed."""
        if self.pk:
            old_instance = (
                Article.objects.filter(pk=self.pk)
                .only("title", "description", "body", "banner_image")
                .first()
            )

            if not (
                old_instance.title == self.title
                and old_instance.description == self.description
                and old_instance.body == self.body
                and old_instance.banner_image == self.banner_image
            ) and hasattr(self, "estimated_reading_time"):
                del self.__dict__["estimated_reading_time"]

    def save(self, *args, **kwargs):
        """Check if need to calculate read time before calling default save."""
        self.check_invalidate_cached_read_time()
        super().save(*args, **kwargs)


class ArticleView(TimestampedModel):
    """Article's views."""

    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="article_views",
    )

    # The user that views this article
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="articles_viewed",
    )
    viewer_ip = models.GenericIPAddressField(
        verbose_name=_("Veiwer IP"),
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("Article View")
        verbose_name_plural = _("Article Views")
        # One article can only be viewed by the same person once
        # But that would result in this article can only being viewed by ananymous user once.
        constraints = [
            models.UniqueConstraint(
                fields=["user", "article", "viewer_ip"],
                name="unqiue_view_per_article_user_ip",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.article.title} viewed by user \
            {self.user.first_name if self.user else 'Anonymous'} from IP {self.viewer_ip}"

    @classmethod
    def record_view(
        cls,
        article: Article,
        user: AbstractBaseUser | None,
        viewer_ip: str,
    ) -> None:
        """
        ArticleView class method to create view instance.

        Args:
            article (Article): Aritcle model instance.
            user (AbstractBaseUser | None): Custom user model instance.
            viewer_ip (str): Viwer IP string.

        """
        cls.objects.get_or_create(
            article=article,
            user=user,
            viewer_ip=viewer_ip,
        )
