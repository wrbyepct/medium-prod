"""Response Adim."""

# ruff: noqa: ANN001, ARG002
from django.contrib import admin

from . import models


@admin.register(models.Response)
class ResponseAdmin(admin.ModelAdmin):
    """Response admin."""

    list_display = ["description", "created_at", "updated_at"]
    list_display_links = ["description"]
    list_filter = ["user__first_name", "user__last_name", "created_at", "updated_at"]
    search_fields = ["article__title"]

    def description(self, obj: models.Response):
        """Return instance string name."""
        return obj.__str__()

    def delete_queryset(self, request, queryset):
        """Trigger .delete() of every instance for the signal to update count."""
        for obj in queryset:
            obj.delete()  # This triggers `post_delete` signals


@admin.register(models.ResponseClap)
class ResponseClapAdmin(admin.ModelAdmin):
    """ResponseClap admin."""

    list_display = ["description", "created_at"]
    list_display_links = ["description"]

    def description(self, obj: models.ResponseClap):
        """Show instance string name."""
        return obj.__str__()
