"""Response urls."""

from django.urls import path

from .views import ResponseListCreateView

urlpatterns = [
    path(
        "top-level-responses/<int:article_id>/",
        ResponseListCreateView.as_views(),
        name="top_level_response_list_create",
    )
]
