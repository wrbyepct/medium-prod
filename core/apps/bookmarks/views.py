"""Bookmark view."""

# ruff: noqa: ANN001, ARG002
# mypy: disable-error-code="annotation-unchecked"

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from .models import ReadingCategory
from .serializers import ReadingCategorySerializer

# # TODO: Implement sorted by bookmark count on non-readingl-list categoreis


class BookmarkCategoryListView(generics.ListAPIView):
    """Show user's bookmark category."""

    serializer_class = ReadingCategorySerializer
    filter_backends = [DjangoFilterBackend]
    ordering = ["-is_reading_list", "-bookmarks"]

    def get_queryset(self):
        """Return only the user's bookmark category."""
        user = self.request.user
        return ReadingCategory.objects.filter(user=user)


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
