"""Bookmark view."""

# ruff: noqa: ANN001, ARG002
from django.db import IntegrityError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter

from core.apps.general.permissions import IsOwnerOrReadOnly
from core.apps.general.utils.article import ArticleUtility

from .filters import BookmarkFilter
from .models import Bookmark
from .paginations import BookmarkPagination
from .serializers import BookmarkSerializer


class BookmarkCreateView(generics.ListCreateAPIView):
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

    def perform_create(self, serializer):
        """Save article by providing article and user in request info."""
        article_id = self.kwargs.get("article_id")
        article = ArticleUtility.get_article(article_id=article_id)

        user = self.request.user

        try:
            serializer.save(article=article, user=user)
        except IntegrityError as already_bookmarked:
            detail = "You have already bookmarked this article."
            raise ValidationError(detail=detail) from already_bookmarked


class BookmarkDestoryView(generics.DestroyAPIView):
    """To unbookmarked."""

    queryset = Bookmark.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = "id"


# Create your views here.
