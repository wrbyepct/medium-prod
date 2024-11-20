"""Profile admin."""

from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Profile Admin Page config."""

    list_display = ["id", "pkid", "user", "country", "city", "phone_number"]
    list_display_links = ["id", "pkid", "user"]
    list_filter = ["id", "pkid"]
