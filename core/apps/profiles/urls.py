"""Profile view urls."""

from django.urls import path

from .views import (
    FollowAPIView,
    FollowersListAPIView,
    FollowingAPIView,
    ProfileDetailAPIView,
    ProfileListAPIView,
    ProfileUpdateAPIView,
    UnfollowAPIView,
)

urlpatterns = [
    path("all/", ProfileListAPIView.as_view(), name="all-profiles"),
    path("me/", ProfileDetailAPIView.as_view(), name="me"),
    path("me/update/", ProfileUpdateAPIView.as_view(), name="update-profile"),
    path("me/followers/", FollowersListAPIView.as_view(), name="me-followers"),
    path("<uuid:user_id>/following/", FollowingAPIView.as_view(), name="following"),
    path("<uuid:user_id>/follow/", FollowAPIView.as_view(), name="follow"),
    path("<uuid:user_id>/unfollow/", UnfollowAPIView.as_view(), name="unfollow"),
]
