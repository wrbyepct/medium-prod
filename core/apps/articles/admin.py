"""Article Admin."""

from django.contrib import admin

from core.apps.ratings.models import Rating
from core.utils.admin import get_model_change_page

from . import models


class RatingsInline(admin.TabularInline):
    """Rating Inline for article."""

    model = Rating
    extra = 1
    readonly_fields = ["edit_link"]

    def edit_link(self, obj: Rating):
        """Return reveresed rating admin page url."""
        return get_model_change_page(
            app_name="ratings",
            model_name="rating",
            obj_id=obj.id,
        )


class ViewInline(admin.TabularInline):
    """View inline for article."""

    model = models.ArticleView
    extra = 1


class ClapInline(admin.TabularInline):
    """Clap Inline field."""

    model = models.Clap
    extra = 1


@admin.register(models.Article)
class ArticleAdmin(admin.ModelAdmin):
    """Article admin."""

    list_display = ["pkid", "id", "author", "title", "slug"]
    list_display_links = ["pkid", "id", "title"]
    list_filter = ["created_at", "updated_at"]
    search_fields = ["body", "title", "tags"]
    ordering = ["-created_at"]
    inlines = [RatingsInline, ViewInline, ClapInline]


@admin.register(models.ArticleView)
class ArticleViewAdmin(admin.ModelAdmin):
    """Custom ArticeView admin."""

    list_display = ["pkid", "id", "article", "user", "viewer_ip"]
    list_display_links = ["pkid", "id", "article"]
    list_filter = ["created_at", "updated_at"]
    search_fields = ["article", "user", "viewer_ip"]


@admin.register(models.Clap)
class ClapAdmin(admin.ModelAdmin):
    """Clap admin."""

    list_display = ["description", "created_at"]
    list_display_links = ["description"]
    list_filter = ["created_at"]
    search_fields = ["article__title", "user__first_name", "user__last_name"]

    def description(self, obj: models.Clap):
        """Return string method of Clap."""
        return obj.__str__()
