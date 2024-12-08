"""Article views."""

# ruff: noqa: ANN001, ARG002
from django.http import Http404
from rest_framework import generics, status
from rest_framework.response import Response

from .models import Article, ArticleView
from .paginations import ArticlePagination
from .permissions import IsOwnerOrReadOnly
from .renderers import ArticleListRenderer, ArticleRenderer
from .serializers import ArticleSerializer


class ArticleCreateListView(generics.ListCreateAPIView):
    """Article view for list and create actions."""

    serializer_class = ArticleSerializer
    pagination_class = ArticlePagination
    renderer_classes = [ArticleListRenderer]

    def get_queryset(self):
        """Return all articles, if user is specified, return all articles belongs to the user."""
        qs = Article.objects.select_related("author").prefetch_related("tags")
        user_id = self.request.query_params.get("user_id")
        if user_id:
            return qs.filter(author=user_id)

        return qs

    def perform_create(self, serializer: ArticleSerializer):
        """Create article with author user info."""
        serializer.save(author=self.request.user)


class ArticleRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """Article Retrieve, Update Destroy view."""

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    renderer_classes = [ArticleRenderer]
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
            request.user if request.user.is_authenticated else None
        )  # None for anonymous user
        ArticleView.record_view(article=article, viewer_ip=viewer_ip, user=user)

        serializer = self.get_serializer(article)
        return Response(serializer.data)
