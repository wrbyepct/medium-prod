"""Bookmark urls."""

from django.urls import path

from .views import BookmarkCreateView

urlpatterns = [
    path(
        "<int:article_id>/",
        BookmarkCreateView.as_view(),
        name="bookmark_create",
    ),
]
