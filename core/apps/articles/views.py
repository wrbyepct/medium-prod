"""Article views."""

# ruff: noqa: ANN001, ARG002
from django.http import Http404
from rest_framework import generics, status
from rest_framework.response import Response

from core.apps.general.permissions import IsOwnerOrReadOnly

from .filters import ArticleFilter
from .models import Article, ArticleView
from .paginations import ArticlePagination
from .serializers import ArticleSerializer


class ArticleCreateListView(generics.ListCreateAPIView):
    """Article view for list and create actions."""

    serializer_class = ArticleSerializer
    pagination_class = ArticlePagination

    filterset_class = ArticleFilter

    # TODO: opitimize for rating average query and views count
    # DONE: Using annotate on manager query
    def get_queryset(self):
        """Return all articles, if user is specified, return all articles belongs to the user."""
        return Article.objects.select_related("author__profile").prefetch_related(
            "tags", "bookmarks"
        )

    def perform_create(self, serializer: ArticleSerializer):
        """Create article with author user info."""
        serializer.save(author=self.request.user)  # This will trigger user query


class ArticleRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """Article Retrieve, Update Destroy view."""

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = "id"

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve article instance and catch Http404 error.

        Record everything in

        Returns
            Response: Return Http404 if article not found, else return article data.

        """
        try:
            article = self.get_object()

        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # record view count
        viewer_ip = request.META.get("REMOTE_ADDR", "")
        user = (
            request.user
            if request.user.is_authenticated
            else None  # None for anonymous user
        )

        ArticleView.record_view(article=article, viewer_ip=viewer_ip, user=user)

        serializer = self.get_serializer(article)
        return Response(serializer.data)
