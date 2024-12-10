"""Rating urls."""

from django.urls import path

from .views import RatingCreateListView, RatingUpdateDestory

urlpatterns = [
    path("", RatingCreateListView.as_view(), name="article_ratings_list_create"),
    path("<int:id>/", RatingUpdateDestory.as_view(), name="rating_update_destory"),
]
