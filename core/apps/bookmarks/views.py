"""Bookmark view."""

# ruff: noqa: ANN001, ARG002
# mypy: disable-error-code="annotation-unchecked"

from rest_framework import generics

from .serializers import ReadingCategorySerializer

# # TODO: Think about how to Re-implement Bookmark view


class BookmarkCreateView(generics.CreateAPIView):
    """View to create a bookmark by adding an article to an existing category."""

    serializer_class = ReadingCategorySerializer

    def get_serializer_context(self):
        """Provide article_id context for serializer."""
        context = super().get_serializer_context()
        context["article_id"] = self.kwargs.get("article_id")
        return context

    def perform_create(self, serializer):
        """Provide user instance in serializer's validated data."""
        serializer.save(user=self.request.user)
