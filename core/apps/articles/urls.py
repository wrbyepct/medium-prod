"""Article url path."""

from django.urls import path

from .views import (
    ArticleCreateListView,
    ArticleRetrieveUpdateDestroyView,
    ClapCreateDestroyView,
)

urlpatterns = [
    path("", ArticleCreateListView.as_view(), name="article_list_create"),
    path(
        "<int:id>/",
        ArticleRetrieveUpdateDestroyView.as_view(),
        name="article_retrieve_update_destroy",
    ),
    path(
        "clap/<int:article_id>/",
        ClapCreateDestroyView.as_view(),
        name="clap_create",
    ),
]
