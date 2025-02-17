"""Bookmark view."""

# ruff: noqa: ANN001, ARG002
# mypy: disable-error-code="annotation-unchecked"

from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.apps.articles.models import Article

from .models import ReadingCategory
from .permissions import IsOwnerOrPublicOnly
from .serializers import ReadingCategorySerializer

# TODO: Implement feature that user can see if the article is bookmarked in what categories.


# TODO: Consider refactor thie view class.
class BookmarkCategoryListView(generics.ListAPIView):
    """GET: Show user's bookmark categories."""

    queryset = ReadingCategory.objects.all()
    serializer_class = ReadingCategorySerializer
    filter_backends = [OrderingFilter]
    ordering = ["-is_reading_list", "-updated_at"]

    # TODO: consider using Materilaized view on this query.
    def get_queryset(self):
        """Return only the user's bookmark category."""
        return self.queryset.filter(user=self.request.user)


class BookmarkCategoryCreateView(generics.CreateAPIView):
    """

    Create a ReadingCategory.

    If article id is provided, add the article the reading category.
    """

    serializer_class = ReadingCategorySerializer

    def get_serializer_context(self):
        """Provide article_id context for serializer."""
        context = super().get_serializer_context()
        context["article_id"] = self.request.query_params.get("article_id", None)
        return context

    def perform_create(self, serializer):
        """Provide user instance in serializer's validated data."""
        serializer.save(user=self.request.user)


class BookmarkCategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """View to retrieve, update and destroy a bookmark category by providing bookmark category slug."""

    queryset = ReadingCategory.objects.all()
    serializer_class = ReadingCategorySerializer
    permission_classes = [IsAuthenticated, IsOwnerOrPublicOnly]
    lookup_field = "slug"


class BookmarkCreateDestoryView(APIView):
    """View to remove a bookmark from a category."""

    def post(self, request, slug, article_id, format=None):
        """Try to add a bookmark from a bookmark category by providng bookmark category slug and article id."""
        article = get_object_or_404(Article, id=article_id)
        category = get_object_or_404(ReadingCategory, user=request.user, slug=slug)

        category.bookmarks.add(article)
        serializer = ReadingCategorySerializer(category)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, slug, article_id, format=None):
        """Try to delete a bookmark from a bookmark category by providng bookmark category slug and article id."""
        article = get_object_or_404(Article, id=article_id)
        category = get_object_or_404(ReadingCategory, user=request.user, slug=slug)

        category.bookmarks.remove(article)

        return Response()
