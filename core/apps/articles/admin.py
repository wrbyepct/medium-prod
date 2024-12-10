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


@admin.register(models.Article)
class ArticleAdmin(admin.ModelAdmin):
    """Article admin."""

    list_display = ["pkid", "author", "title", "slug", "views"]
    list_display_links = ["pkid", "title"]
    list_filter = ["created_at", "updated_at"]
    search_fields = ["body", "title", "tags"]
    ordering = ["-created_at"]
    inlines = [RatingsInline]


@admin.register(models.ArticleView)
class ArticleViewAdmin(admin.ModelAdmin):
    """Custom ArticeView admin."""

    list_display = ["pkid", "article", "user", "viewer_ip"]
    list_display_links = ["pkid", "article"]
    list_filter = ["created_at", "updated_at"]
    search_fields = ["article", "user", "viewer_ip"]
