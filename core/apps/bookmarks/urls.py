"""Bookmark urls."""

from django.urls import path

from .views import BookmarkCategoryListView, BookmarkCreateView

urlpatterns = [
    path(
        "categories/", BookmarkCategoryListView.as_view(), name="bookmark_category_list"
    ),
    path(
        "<int:article_id>/",
        BookmarkCreateView.as_view(),
        name="bookmark_create",
    ),
]
