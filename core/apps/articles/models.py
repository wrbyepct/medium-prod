"""Article app model."""

# mypy: disable-error-code="var-annotated,attr-defined"
# ruff: noqa: D105
from __future__ import annotations

from functools import partial
from typing import TYPE_CHECKING

from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager

from core.apps.general.models import TimestampedModel
from core.tools.hash import generate_hashed_slug
from core.tools.image import generate_file_path

from .managers import ArticleManager
from .services.read_time_engine import ArticleReadTimeEngine

if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractBaseUser

User = get_user_model()

upload_to = partial(generate_file_path, app_name="articles")


class Clap(TimestampedModel):
    """Article claps model."""

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
        upload_to=upload_to,
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
