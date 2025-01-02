"""Rating urls."""

from django.urls import path

from .views import RatingCreateListView, RatingUpdateDestoryView

urlpatterns = [
    path(
        "<int:article_id>/",
        RatingCreateListView.as_view(),
        name="article_ratings_list_create",
    ),
    path(
        "edit/<int:id>/",
        RatingUpdateDestoryView.as_view(),
        name="rating_update_destory",
    ),
]
