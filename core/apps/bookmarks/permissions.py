"""Bookmark permissions."""

import logging

from rest_framework.permissions import SAFE_METHODS, BasePermission

logger = logging.getLogger(__name__)


class IsOwnerOrPublicOnly(BasePermission):
    """Bookmark category permission."""

    def has_object_permission(self, request, view, obj):
        """
        If a user is not owner, they can only access those which are public.

        All users only have read permission to their own 'Reading list' category.
        """
        if request.method in SAFE_METHODS and request.user != obj.user:
            return not obj.is_private

        # Deny deletion of 'Reading list' category
        if obj.is_reading_list and request.method == "DELETE":
            return False
        return request.user == obj.user
