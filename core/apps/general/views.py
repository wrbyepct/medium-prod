"""General view."""

# ruff: noqa: ANN001, ARG002, D301
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthCheckView(APIView):
    """View for checking API health."""

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        """Return healthy message and 200 ok."""
        return Response({"message": "API is healthy!"}, status=status.HTTP_200_OK)
