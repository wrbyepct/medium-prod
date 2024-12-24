"""Response Adim."""

from django.contrib import admin

from . import models


@admin.register(models.Response)
class ResponseAdmin(admin.ModelAdmin):
    """Response admin."""

    list_display = ["id", "description", "created_at", "updated_at"]
    list_display_links = ["id", "description"]
    list_filter = ["user__first_name", "user__last_name", "created_at", "updated_at"]
    search_fields = ["article__title"]

    def description(self, obj: models.Response):
        """Return instance string name."""
        return obj.__str__()
