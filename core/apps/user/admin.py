"""Account app admin page."""

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core.apps.bookmarks.models import ReadingCategory

User = get_user_model()


class ReadingCategoryInline(admin.TabularInline):
    """Bookmark Category Inline."""

    model = ReadingCategory
    extra = 1


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """User admin BaseUserAdmin class."""

    inlines = [ReadingCategoryInline]
    ordering = ["email"]
    list_display = [
        "pkid",
        "id",
        "email",
        "first_name",
        "last_name",
        "is_active",
        "is_staff",
    ]
    list_display_links = [
        "email",
        "pkid",
        "id",
    ]
    list_filter = ["is_active", "is_staff", "email"]

    search_fields = ["first_name", "last_name", "email"]

    readonly_fields = ["date_joined"]

    fieldsets = (
        (
            _("Login Credentials"),
            {"fields": ("email", "password")},
        ),
        (
            _("Persoanl Info"),
            {"fields": ("first_name", "last_name")},
        ),
        (
            _("Permissions and Groups"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "user_permissions",
                    "groups",
                ),
            },
        ),
        (
            _("Important Dates"),
            {"fields": ("last_login", "date_joined")},
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
