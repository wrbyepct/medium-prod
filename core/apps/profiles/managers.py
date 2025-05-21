"""Profile Model Manager."""

from django.db import models


class ProfileQuerySet(models.QuerySet):
    """Custom Profile queryset."""

    def join_user_table(self):
        """Return qs by joining table with user."""
        return self.select_related("user")

    def follow_preview_info(self):
        """
        Get only the necessary columns for follower/following info.

        Columns:
           - "profile_photo"
           - "about_me"
           - "twitter_handle"
           - "user__first_name"
           - "user__last_name"

        By selecting joined table from user.
        """
        return (
            self.join_user_table()
            .only(
                "profile_photo",
                "about_me",
                "twitter_handle",
                "user__first_name",
                "user__last_name",
            )
            .order_by("user__first_name")
        )


class ProfileManager(models.Manager):
    """Custom profile manager."""

    def get_queryset(self):
        """Get orignal qs."""
        return ProfileQuerySet(model=self.model, using=self._db)
