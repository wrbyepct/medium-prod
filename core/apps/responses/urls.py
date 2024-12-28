"""Response urls."""

from django.urls import path

from .views import (
    ReplyListCreateView,
    ResponseClapCreateDestroyView,
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
        "child-replies/<int:reply_to_id>/",
        ReplyListCreateView.as_view(),
        name="next_child_replies_list_create",
    ),
    path(
        "<int:id>/", ResponseUpdateDestroyView.as_view(), name="response_update_destroy"
    ),
    path(
        "clap/<int:response_id>/",
        ResponseClapCreateDestroyView.as_view(),
        name="response_clap_create_destroy",
    ),
]
