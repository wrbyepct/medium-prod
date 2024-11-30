"""Profile admin."""

from django.contrib import admin

from .models import Profile


class FollowingInline(admin.TabularInline):
    """Profile's following inline."""

    model = Profile.followers.through
    fk_name = "to_profile"
    extra = 1
    verbose_name = "following"


class FollowersInline(admin.TabularInline):
    """Profile's followers inline."""

    model = Profile.followers.through
    fk_name = "from_profile"
    extra = 1
    verbose_name = "follower"


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Profile Admin Page config."""

    list_display = ["id", "pkid", "user", "country", "city", "phone_number"]

    list_display_links = ["id", "pkid", "user"]
    list_filter = ["id", "pkid"]

    inlines = [FollowingInline, FollowersInline]
