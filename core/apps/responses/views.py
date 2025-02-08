"""Response views."""

# ruff: noqa: ANN001, ARG002
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response as Res
from rest_framework.views import APIView

from core.apps.articles.models import Article
from core.apps.general.permissions import IsOwnerOrReadOnly

from .models import Response, ResponseClap
from .paginations import ResponsePagination
from .serializers import ResponseSerializer


class BaseResponseListCreateView(generics.ListCreateAPIView):
    """Base Response List Create View."""

    serializer_class = ResponseSerializer
    pagination_class = ResponsePagination
    filter_backends = [OrderingFilter]


class ResponseListCreateView(BaseResponseListCreateView):
    """Get top-level responses of an article."""

    ordering_fields = ["claps_count", "replies_count", "created_at"]
    ordering = ["-claps_count", "-replies_count", "-created_at", "-updated_at"]

    def get_queryset(self):
        """Get top-level responses of an article."""
        article_id = self.kwargs.get("article_id")

        return Response.objects.filter(article__id=article_id, parent__isnull=True)

    def perform_create(self, serializer: ResponseSerializer):
        """Create top-level response with article and user instance."""
        article_id = self.kwargs.get("article_id")
        article = get_object_or_404(Article.objects.only("id"), id=article_id)
        user = self.request.user
        serializer.save(article=article, user=user)


class ReplyListCreateView(BaseResponseListCreateView):
    """Get immediate child replies of a specified response."""

    ordering_fields = ["-claps_count", "-created_at"]
    ordering = ["-claps_count", "-created_at", "-updated_at"]

    def get_queryset(self):
        """Get child replies from a parent response to an article."""
        parent_id = self.kwargs.get("reply_to_id")

        return Response.objects.filter(parent__id=parent_id)

    def perform_create(self, serializer: ResponseSerializer):
        """Create next-child response with article and user and parent response instance."""
        parent_id = self.kwargs.get("reply_to_id")
        parent_response = get_object_or_404(Response.objects.only("id"), id=parent_id)
        article = parent_response.article
        user = self.request.user
        serializer.save(article=article, user=user, parent=parent_response)


class ResponseUpdateDestroyView(generics.UpdateAPIView, generics.DestroyAPIView):
    """Update or delete a reponse by provding id."""

    queryset = Response.objects.all()
    serializer_class = ResponseSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = "id"


class ResponseClapCreateDestroyView(APIView):
    """Clap or un clap a response by providing response id."""

    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def post(self, request, response_id, format=None):
        """Clap a response."""
        response = get_object_or_404(Response, id=response_id)

        try:
            ResponseClap.objects.create(user=request.user, response=response)
            res = {
                "data": {
                    "message": f"Successfully clapped the response: {response_id}"
                },
                "status": status.HTTP_201_CREATED,
            }
        except IntegrityError:
            res = {
                "data": {"message": "You have already clapped this response."},
                "status": status.HTTP_400_BAD_REQUEST,
            }
        return Res(**res)

    def delete(self, request, response_id, format=None):
        """Unclap a response."""
        res_clap = get_object_or_404(
            ResponseClap, response=response_id, user=request.user
        )
        res_clap.delete()
        # TODO: Figure out why it still shows 200 instead of 204
        return Res(status=status.HTTP_204_NO_CONTENT, data=None)
