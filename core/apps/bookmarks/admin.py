"""Bookmark admin."""

from django.contrib import admin

from .models import Bookmark, BookmarksInCategories, ReadingCategory


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    """Bookmark admin."""

    list_display = ["id", "description", "created_at"]
    list_display_links = ["id", "description"]
    search_fields = ["user__first_name", "user__last_name"]

    def description(self, obj: Bookmark):
        """Show bookmark model's __str__ name."""
        return obj.__str__()


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
