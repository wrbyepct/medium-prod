"""Bookmark admin."""

from django.contrib import admin

from .models import BookmarksInCategories, ReadingCategory


class BookmarkInline(admin.TabularInline):
    """Bookmark inline."""

    model = BookmarksInCategories
    extra = 1


@admin.register(ReadingCategory)
class ReadingCategoryAdmin(admin.ModelAdmin):
    """Reading Category admin."""

    list_display = ["id", "title", "user_full_name"]
    list_display_links = ["id", "title"]
    inlines = [BookmarkInline]

    def user_full_name(self, obj: ReadingCategory):
        """Return user full name."""
        return obj.user.full_name
