"""Bookmark admin."""

from django.contrib import admin

from .models import Bookmark


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    """Bookmark admin."""

    list_display = ["id", "description", "created_at"]
    list_display_links = ["id", "description"]
    search_fields = ["user__first_name", "user__last_name"]

    def description(self, obj: Bookmark):
        """Show bookmark model's __str__ name."""
        return obj.__str__()
