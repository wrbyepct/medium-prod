"""Bookmark urls."""

from django.urls import path

from .views import BookmarkCreateView, BookmarkDestoryView

urlpatterns = [
    path("", BookmarkCreateView.as_view(), name="bookmark_list"),
    path("<int:article_id>/", BookmarkCreateView.as_view(), name="bookmark_create"),
    path("remove/<int:id>/", BookmarkDestoryView.as_view(), name="bookmark_destroy"),
]
