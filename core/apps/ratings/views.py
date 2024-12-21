"""Ratings views."""

# ruff: noqa: ANN001, ARG002
import logging

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from core.apps.general.permissions import IsOwnerOrReadOnly
from core.apps.general.utils.article import ArticleUtility

from .exceptions import YouCannotRateArticleAgain
from .models import Rating
from .serializers import RatingSerializer

logger = logging.getLogger(__name__)
# List articles all review
# update my rating
# Create my rating
# Delte my rating


class RatingCreateListView(generics.ListCreateAPIView):
    """Rating Create & List view."""

    serializer_class = RatingSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = {
        "rating": ["exact", "gte", "lte"],
    }
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]

    def get_queryset(self):
        """Get queryset based on article id."""
        article = self.get_article()
        return article.ratings.select_related("user", "article")

    def list(self, request, *args, **kwargs):
        """Get all ratings of the given article."""
        # filter_queryset() furhter applies filter backends' query
        # E.g., rating greater than or equal to
        qs = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(qs, many=True)
        formatted_response = {
            "total_ratings_count": qs.count(),
            "rating_list": serializer.data,
        }
        return Response(formatted_response)

    def perform_create(self, serializer):
        """Get article and request user first and then create the rating."""
        article_id = self.request.query_params.get("article_id", None)
        article = ArticleUtility.get_article(article_id=article_id)
        user = self.request.user

        rating = Rating.objects.filter(user=user, article=article).exists()
        if rating:
            raise YouCannotRateArticleAgain

        serializer.save(user=user, article=article)


class RatingUpdateDestory(generics.RetrieveUpdateDestroyAPIView):
    """Rating Update and Destory view."""

    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = "id"
