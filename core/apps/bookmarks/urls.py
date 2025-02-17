"""Bookmark urls."""

from django.urls import path

from .views import (
    BookmarkCategoryCreateView,
    BookmarkCategoryListView,
    BookmarkCategoryRetrieveUpdateDestroyView,
    BookmarkCreateDestoryView,
)

urlpatterns = [
    path(
        "categories/",
        BookmarkCategoryListView.as_view(),
        name="bookmark_category_list",
    ),
    path(
        "categories/create/",
        BookmarkCategoryCreateView.as_view(),
        name="bookmark_create",
    ),
    path(
        "category/<slug:slug>/",
        BookmarkCategoryRetrieveUpdateDestroyView.as_view(),
        name="bookmark_category_retrieve_update_destroy",
    ),
    path(
        "category/<slug:slug>/<uuid:article_id>/",
        BookmarkCreateDestoryView.as_view(),
        name="bookmark_create_delete",
    ),
]
