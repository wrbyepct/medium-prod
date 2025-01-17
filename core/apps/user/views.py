"""Account view."""

from django.contrib.auth import get_user_model
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerializer


class CustomUserDetailsView(RetrieveUpdateAPIView):
    """Retrieve or update your user information."""

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """Return user instance."""
        return self.request.user

    def get_queryset(self):
        """Return empty set of user."""
        return get_user_model().objects.none()
