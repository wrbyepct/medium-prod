"""Article Admin."""

from django.contrib import admin

from . import models


@admin.register(models.Article)
class ArticleAdmin(admin.ModelAdmin):
    """Article admin."""

    list_display = ["pkid", "author", "title", "slug", "views"]
    list_display_links = ["pkid", "title"]
    list_filter = ["created_at", "updated_at"]
    search_fields = ["body", "title", "tags"]
    ordering = ["-created_at"]


@admin.register(models.ArticleView)
class ArticleViewAdmin(admin.ModelAdmin):
    """Custom ArticeView admin."""

    list_display = ["pkid", "article", "user", "viewer_ip"]
    list_display_links = ["pkid", "article"]
    list_filter = ["created_at", "updated_at"]
    search_fields = ["article", "user", "viewer_ip"]
