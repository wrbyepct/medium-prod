"""Rating urls."""

from django.urls import path

from .views import RatingCreateListView, RatingUpdateDestoryView

urlpatterns = [
    path(
        "<uuid:article_id>/",
        RatingCreateListView.as_view(),
        name="article_ratings_list_create",
    ),
    path(
        "edit/<uuid:id>/",
        RatingUpdateDestoryView.as_view(),
        name="rating_update_destory",
    ),
]
