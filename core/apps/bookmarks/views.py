"""Bookmark view."""

# ruff: noqa: ANN001, ARG002
# mypy: disable-error-code="annotation-unchecked"

from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.apps.articles.models import Article

from .exceptions import SignalProcessingError
from .models import ReadingCategory
from .permissions import IsOwnerOrPublicOnly
from .serializers import ReadingCategorySerializer


class BookmarkCategoryListView(generics.ListAPIView):
    """Show user's bookmark category."""

    serializer_class = ReadingCategorySerializer

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


class BookmarkCategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """View to retrieve, update and destroy a bookmark category."""

    queryset = ReadingCategory.objects.all()
    serializer_class = ReadingCategorySerializer
    permission_classes = [IsOwnerOrPublicOnly]
    lookup_field = "slug"


class BookmarkDestoryView(APIView):
    """View to remove a bookmark from a category."""

    def delete(self, request, slug, article_id, format=None):
        """Try to delete a bookmark from a bookmark category."""
        article = get_object_or_404(Article, id=article_id)
        category = get_object_or_404(ReadingCategory, user=request.user, slug=slug)
        try:
            category.bookmarks.remove(article)
        except SignalProcessingError:
            return Response(
                {"message": "Oops, something went wrong."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return Response(data=None, status=status.HTTP_204_NO_CONTENT)
