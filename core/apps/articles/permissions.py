"""Article permissions."""

from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwnerOrReadOnly(BasePermission):
    """Custom Article permission."""

    def has_object_permission(self, request, view, obj):
        """Check if the article belongs to the user."""
        if request.method in SAFE_METHODS:
            return True
        return request.user == obj.author
