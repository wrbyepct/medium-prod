"""Article url path."""

from django.urls import path

from .views import ArticleCreateListView, ArticleRetrieveUpdateDestroyView

urlpatterns = [
    path("", ArticleCreateListView.as_view(), name="article_list_create"),
    path(
        "<int:id>/",
        ArticleRetrieveUpdateDestroyView.as_view(),
        name="article_retrieve_update_destroy",
    ),
]
