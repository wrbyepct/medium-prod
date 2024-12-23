"""Bookmark urls."""

from django.urls import path

from .views import BookmarkCreateDestoryView, BookmarkListView

urlpatterns = [
    path("", BookmarkListView.as_view(), name="bookmark_list"),
    path(
        "<int:article_id>/",
        BookmarkCreateDestoryView.as_view(),
        name="bookmark_create_destroy",
    ),
]
