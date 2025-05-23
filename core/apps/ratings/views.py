"""Ratings views."""

# ruff: noqa: ANN001, ARG002
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated

from core.apps.articles.models import Article
from core.apps.general.permissions import IsOwnerOrReadOnly

from .exceptions import YouCannotRateArticleAgain
from .models import Rating
from .paginations import RatingPagination
from .serializers import RatingSerializer

# List articles all review
# update my rating
# Create my rating
# Delte my rating


class RatingCreateListView(generics.ListCreateAPIView):
    """Create rating on an aritcle & show all ratings of an article."""

    serializer_class = RatingSerializer
    pagination_class = RatingPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = {
        "rating": ["exact", "gte", "lte"],
    }
    ordering_fields = ["created_at", "rating"]
    ordering = ["-rating", "-created_at"]

    def get_queryset(self):
        """Get queryset based on article id."""
        article_id = self.kwargs.get("article_id")

        article = get_object_or_404(Article.objects.only("id"), id=article_id)
        return Rating.objects.filter(article=article)

    def perform_create(self, serializer):
        """Get article and request user first and then create the rating."""
        article_id = self.kwargs.get("article_id")
        article = get_object_or_404(Article.objects.only("id"), id=article_id)
        user = self.request.user
        rating = Rating.objects.filter(user=user, article=article).exists()
        if rating:
            raise YouCannotRateArticleAgain

        serializer.save(user=user, article=article)


class RatingUpdateDestoryView(generics.UpdateAPIView, generics.DestroyAPIView):
    """Edit or delete a rating."""

    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = "id"
