"""Bookmark view."""

# ruff: noqa: ANN001, ARG002
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.views import APIView

from core.apps.articles.models import Article
from core.apps.general.permissions import IsOwnerOrReadOnly

from .filters import BookmarkFilter
from .models import Bookmark
from .paginations import BookmarkPagination
from .serializers import BookmarkSerializer


# TODO: Think about how to Re-implement Bookmark view
class BookmarkListView(generics.ListAPIView):
    """Bookmark list create view."""

    serializer_class = BookmarkSerializer
    pagination_class = BookmarkPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = BookmarkFilter
    ordering_fields = ["created_at", "article__created_at"]  # Allowed ordering fields

    def get_queryset(self):
        """Get all user's bookmarks."""
        user = self.request.user
        # Avoid using "user.bookmarks.select_related("article", "article__author")"
        # Because we might change the related name "bookmarks" to other name.
        return Bookmark.objects.filter(user=user).select_related(
            "article", "article__author"
        )


class BookmarkCreateDestoryView(APIView):
    """Bookmark create & destroy view."""

    permission_classes = [IsOwnerOrReadOnly]

    def post(self, request, article_id, format=None):
        """
        Create boomark using user and specified article.

        Returns
            404 - If the specified article cannot be found
            400 - If the user has already boomarked the article
            201 - Successfully creatd.

        """
        # How should i implement post using general api view.
        article = get_object_or_404(Article, id=article_id)
        user = request.user
        try:
            Bookmark.objects.create(user=user, article=article)
            detail = f"Successfully bookmarked the article: {article.title}"
            return Response({"message": detail}, status=status.HTTP_201_CREATED)
        except IntegrityError:
            detail = "You already bookmarked the article"
            return Response({"message": detail}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, article_id, format=None):
        """
        Unbookmark an article.

        Returns
            404 - If the specified article cannot be found
            204 - Successfully removed, no content.

        """
        clap = get_object_or_404(Bookmark, user=request.user, article=article_id)
        clap.delete()
        # TODO: Figure out why it still shows 200 instead of 204
        return Response(data=None, status=status.HTTP_204_NO_CONTENT)
