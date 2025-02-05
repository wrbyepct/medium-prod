"""Article views."""

# ruff: noqa: ANN001, ARG002, D301
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.apps.general.permissions import IsOwnerOrReadOnly

from .filters import ArticleFilter
from .models import Article, ArticleView, Clap
from .paginations import ArticlePagination
from .serializers import ArticleSerializer
from .services.es import full_text_search


class ArticleListCreateView(generics.ListCreateAPIView):
    """
    Show all articles, 10 results per page(You can request 20 results at maximum).

    You can filter results by:

        1. Full-text search fields(Elasticsarch):
            - title
            - description
            - body
            - slug
            - author.first_name
            - author.last_name
            - tags

        2. Exact match:
            - tags

        3. Time range:
            - created_at_after (e.g.: 2025-01-01)
            - created_at_before (e.g.: 2024-12-31)

        4. Ordering:
            - ordering: (specify "created_at" or "-created_at")

    """

    serializer_class = ArticleSerializer
    pagination_class = ArticlePagination
    filterset_class = ArticleFilter
    filter_backends = [OrderingFilter]
    ordering_fields = ["created_at", "title"]
    # We already set the default to DjangoFilterBackend at the settings.py

    # TODO: Try to optimize for TaggableManager's tag insertion

    # TODO: Think how to persoalize article feed.

    def handle_fulltext_search(self):
        """Use Elasticsearch to return filtered article ids if search term is provided, else return None."""
        search_term = self.request.query_params.get("search", None)
        if search_term:
            return full_text_search(search_term)
        return None

    def get_queryset(self):
        """Return all articles, if search term is provided, return all articles based on the search terms."""
        qs = Article.statistic_objects.all()
        article_ids = self.handle_fulltext_search()
        if article_ids:
            return qs.filter(id__in=article_ids)

        return qs

    def perform_create(self, serializer: ArticleSerializer):
        """Create article with author user info."""
        serializer.save(author=self.request.user)  # This will trigger user query


class ArticleRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or destory an artice by providing article id."""

    queryset = Article.statistic_objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = "id"

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve article instance, catch Http404 error if article does not exist.

        Record Article view.

        Returns
            Response: Return Http404 if article not found, else return article data.

        """
        article = self.get_object()
        # record view count
        viewer_ip = request.META.get("REMOTE_ADDR", "")
        user = (
            request.user
            if request.user.is_authenticated
            else None  # None for anonymous user
        )

        ArticleView.record_view(article=article, viewer_ip=viewer_ip, user=user)
        article = self.get_object()  # get newest view counts

        serializer = self.get_serializer(article)
        return Response(serializer.data)


class ClapCreateDestroyView(APIView):
    """Clap / Unclap an article."""

    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def post(self, request, article_id, format=None):
        """
        Create clap using user and specified article.

        Return: \n
            404 - If the specified article cannot be found. \n
            400 - If the user has already clapped the article. \n
            201 - Successfully creatd.

        """
        article = get_object_or_404(Article.objects.only("id", "title"), id=article_id)
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

        Return: \n
            404 - If the specified article cannot be found. \n
            204 - Successfully removed, no content. \n

        """
        article = get_object_or_404(Article, id=article_id)
        clap = get_object_or_404(Clap, user=request.user, article=article)

        clap.delete()

        message = "Successfully unclap the article."
        return Response({"message": message})
