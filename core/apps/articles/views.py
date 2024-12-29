"""Article views."""

# ruff: noqa: ANN001, ARG002
from django.db import IntegrityError
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.apps.general.permissions import IsOwnerOrReadOnly

from .filters import ArticleFilter
from .models import Article, ArticleView, Clap
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
            "tags", "claps__user"
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
        Retrieve article instance, catch Http404 error if article does not exist.

        Record Article view.

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


class ClapCreateDestroyView(APIView):
    """Clap create or destroy view."""

    permission_classes = [IsOwnerOrReadOnly]

    def post(self, request, article_id, format=None):
        """
        Create clap using user and specified article.

        Returns
            404 - If the specified article cannot be found
            400 - If the user has already clapped the article
            201 - Successfully creatd.

        """
        # How should i implement post using general api view.
        article = get_object_or_404(Article, id=article_id)
        user = request.user
        try:
            Clap.objects.create(user=user, article=article)
            detail = f"Successfully clapped the article: {article.title}"
            return Response({"message": detail}, status=status.HTTP_201_CREATED)
        except IntegrityError:
            detail = "You already clapped the article"
            return Response({"message": detail}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, article_id, format=None):
        """
        Unclapped an article.

        Returns
            404 - If the specified article cannot be found
            204 - Successfully removed, no content.

        """
        clap = get_object_or_404(Clap, user=request.user, article=article_id)
        clap.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
