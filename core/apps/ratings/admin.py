"""Ratings admin."""

# mypy: disable-error-code="attr-defined"
# ruff: noqa: ANN001
from django.contrib import admin

from core.utils.admin import get_model_change_page

from .models import Rating


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Rating admin."""

    list_display = ["rating", "custom_display", "user_full_name"]
    list_display_links = ["custom_display"]
    readonly_fields = ["article_link", "user_profile", "created_at", "updated_at"]
    search_fields = ["article__title", "user__first_name", "user__last_name"]
    list_filter = ["rating", "created_at", "updated_at"]

    def user_full_name(self, obj):
        """Return rating user's full name."""
        return obj.user.full_name

    @admin.display(description="Rated by")
    def custom_display(self, obj):
        """Display Rated by <user.first_name> on article <article.title>."""
        return f"'{obj.user.first_name}' on article: {obj.article.title}"

    def article_link(self, obj):
        """Return the reviewed article link."""
        return get_model_change_page(
            app_name="articles",
            model_name="article",
            obj_id=obj.article.id,
        )

    def user_profile(self, obj):
        """Return the user's profile who rated the article."""
        return get_model_change_page(
            app_name="profiles",
            model_name="profile",
            obj_id=obj.user.profile.id,
        )
