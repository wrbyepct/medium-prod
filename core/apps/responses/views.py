"""Response views."""

from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.filters import OrderingFilter

from core.apps.articles.models import Article
from core.apps.general.permissions import IsOwnerOrReadOnly
from core.utils.article import ResponseUtility

from .models import Response
from .paginations import ResponsePagination
from .serializers import ResponseSerializer


class ResponseListCreateView(generics.ListCreateAPIView):
    """Response View."""

    serializer_class = ResponseSerializer
    pagination_class = ResponsePagination
    filter_backends = [OrderingFilter]
    ordering = ["-claps_count", "-created_at", "-updated_at"]

    def get_queryset(self):
        """Get top-level responses of an article."""
        article_id = self.kwargs.get("article_id")

        return (
            Response.objects.select_related("article", "user", "parent")
            .only(
                "id",
                "content",
                "claps_count",
                "replies_count",
                "user__first_name",
                "user__last_name",
                "article__id",
                "parent__id",
            )
            .filter(article__id=article_id, parent__isnull=True)
        )

    def perform_create(self, serializer: ResponseSerializer):
        """Create top-level response with article and user instance."""
        article_id = self.kwargs.get("article_id")
        article = get_object_or_404(Article, id=article_id)
        user = self.request.user
        serializer.save(article=article, user=user)


class ReplyListCreateView(generics.ListCreateAPIView):
    """Response Create view."""

    serializer_class = ResponseSerializer
    pagination_class = ResponsePagination
    filter_backends = [OrderingFilter]
    ordering = ["-claps_count", "-created_at", "-updated_at"]

    def get_queryset(self):
        """Get child replies from a parent response to an article."""
        parent_id = self.kwargs.get("reply_to_id")
        get_object_or_404(Response, id=parent_id)
        return Response.objects.filter(parent__id=parent_id)

    def perform_create(self, serializer: ResponseSerializer):
        """Create next-child response with article and user and parent response instance."""
        parent_id = self.kwargs.get("reply_to_id")
        parent_response = ResponseUtility.get_response(response_id=parent_id)
        article = parent_response.article
        user = self.request.user
        serializer.save(article=article, user=user, parent=parent_response)


class ResponseUpdateDestroyView(generics.UpdateAPIView, generics.DestroyAPIView):
    """Response Update Destroy View."""

    queryset = Response.objects.all()
    serializer_class = ResponseSerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = "id"
