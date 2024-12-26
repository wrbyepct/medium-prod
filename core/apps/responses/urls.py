"""Response urls."""

from django.urls import path

from .views import (
    ReplyListCreateView,
    ResponseListCreateView,
    ResponseUpdateDestroyView,
)

urlpatterns = [
    path(
        "top-level-responses/<int:article_id>/",
        ResponseListCreateView.as_view(),
        name="top_level_response_list_create",
    ),
    path(
        "next-child-replies/<int:reply_to_id>/",
        ReplyListCreateView.as_view(),
        name="next_child_replies_list_create",
    ),
    path(
        "<int:id>/", ResponseUpdateDestroyView.as_view(), name="response_update_destroy"
    ),
]
