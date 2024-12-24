"""Response views."""

from rest_framework import generics
from rest_framework.filters import OrderingFilter

from core.utils.article import ArticleUtility

from .models import Response
from .serializers import ResponseSerializer


class ResponseListCreateView(generics.ListCreateAPIView):
    """Response View."""

    serializer_class = ResponseSerializer
    filter_backends = [OrderingFilter]
    ordering = ["-claps_count", "-created_at"]

    def get_queryset(self):
        """Get top-level responses of an article."""
        article_id = self.kwargs.get("article_id")
        article = ArticleUtility.get_article(article_id=article_id)
        return Response.objects.filter(article=article, parent__isnull=True)

    def perform_create(self, serializer: ResponseSerializer):
        """Create response with article and user instance."""
        article_id = self.kwargs.get("article_id")
        article = ArticleUtility.get_article(article_id=article_id)
        user = self.request.user
        serializer.save(article=article, user=user)


class ResponseCreateView(generics.CreateAPIView):
    """Response Create view."""

    serializer_class = ResponseSerializer
