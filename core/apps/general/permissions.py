"""Custom permissions."""

from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwnerOrReadOnly(BasePermission):
    """Checking if it's the owner of the instnace."""

    def has_object_permission(self, request, view, obj):
        """Return True if the requester is the same of the modifying onwer."""
        if request.method in SAFE_METHODS:
            return True
        return request.user == obj.user
