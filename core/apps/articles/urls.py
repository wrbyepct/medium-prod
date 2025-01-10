"""Article url path."""

from django.urls import path

from .views import (
    ArticleListCreateView,
    ArticleRetrieveUpdateDestroyView,
    ClapCreateDestroyView,
)

urlpatterns = [
    path("", ArticleListCreateView.as_view(), name="article_list_create"),
    path(
        "<uuid:id>/",
        ArticleRetrieveUpdateDestroyView.as_view(),
        name="article_retrieve_update_destroy",
    ),
    path(
        "clap/<uuid:article_id>/",
        ClapCreateDestroyView.as_view(),
        name="clap_create",
    ),
]
