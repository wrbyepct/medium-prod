"""Profile views."""

from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from core.tools.email import inform_followed

from .models import Profile
from .paginations import ProfilePagination
from .renderers import ProfileListRenderer, ProfileRenderer
from .serializers import FollowingSerializer, ProfileSerializer, UpdateProfileSerializer

# ruff: noqa: A002, ANN001, ARG002

User = get_user_model()


class ProfileListAPIView(generics.ListAPIView):
    """Profile List API View."""

    queryset = Profile.objects.select_related("user")
    serializer_class = ProfileSerializer
    pagination_class = ProfilePagination
    renderer_classes = [ProfileListRenderer]


class ProfileDetailAPIView(generics.RetrieveAPIView):
    """Profile detail API view."""

    serializer_class = ProfileSerializer
    renderer_classes = [ProfileRenderer]

    def get_queryset(self):
        """
        Optimize query by joining the user table.

        So you don't have to query through profile for user.
        """
        return Profile.objects.select_related("user")

    def get_object(self):
        """Get object filter by requesting user."""
        user = self.request.user
        return self.get_queryset().get(user=user)


class ProfileUpdateAPIView(generics.UpdateAPIView):
    """Profile API view for partial update."""

    serializer_class = UpdateProfileSerializer
    renderer_classes = [ProfileRenderer]

    def get_object(self):
        """
        Get profile directly through user's profile field.

        So we don't need to query through profile objects with id like default.
        """
        return self.request.user.profile


class BaseFollowListView(generics.ListAPIView):
    """Template view for Following/Followers list view."""

    serializer_class = FollowingSerializer

    def get_queryset(self):
        """
        Return instances with necessary columns.

        Columns:
           - "profile_photo"
           - "about_me"
           - "twitter_handle"
           - "user__first_name"
           - "user__last_name"


        By selecting joined table from user.
        """
        return Profile.objects.only(
            "profile_photo",
            "about_me",
            "twitter_handle",
            "user__first_name",
            "user__last_name",
        ).select_related("user")

    def get(self, request, *args, **kwargs):
        """Return formatted response: follow_type_count, follow_type data."""
        response = super().get(request, *args, **kwargs)
        data = response.data
        follow_type = self.follow_type
        formatted_response = {
            f"{follow_type}_count": len(data),
            follow_type: response.data,
        }
        return Response(formatted_response)


class FollowersListAPIView(BaseFollowListView):
    """Get user's followers by specifying user uuid."""

    follow_type = "followers"

    def get_queryset(self):
        """Filter results by selecting those who follow the user."""
        user_id = self.kwargs.get("user_id")
        return super().get_queryset().filter(following__user__id=user_id)


class FollowingListAPIView(BaseFollowListView):
    """Get user's following by specifying user uuid."""

    follow_type = "following"

    def get_queryset(self):
        """Filter results by selecting those whose followers contain the user."""
        user_id = self.kwargs.get("user_id")
        return super().get_queryset().filter(followers__user__id=user_id)


class FollowAPIView(APIView):
    """Follow API View."""

    def post(self, request, user_id, format=None, *args, **kwargs):
        """To follow a user."""
        try:
            to_follow_profile = Profile.objects.get(user__id=user_id)

        except Profile.DoesNotExist as profile_not_found:
            detail = "You can't follow a profile that does not exist."
            raise NotFound(detail=detail) from profile_not_found

        if request.user.id == user_id:
            return Response(
                {"message": "You can't follow yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        requesting_profile = request.user.profile
        if requesting_profile.has_followed(to_follow_profile):
            return Response(
                {"message": "You already followed that user."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        requesting_profile.follow(to_follow_profile)

        email_data = {
            "being_followed_user_first_name": to_follow_profile.user.first_name,
            "to_email": to_follow_profile.user.email,
            "user_fullname": requesting_profile.user.full_name,
        }

        inform_followed(**email_data)  # TODO: Will send email fail?

        return Response(
            {
                "message": f"You successfully followed {to_follow_profile.user.full_name}.",
            },
            status=status.HTTP_200_OK,
        )


class UnfollowAPIView(APIView):
    """View to unfollow a user."""

    def post(self, request, user_id, *args, **kwargs):
        """To unfollow a user."""
        try:
            to_unfollow_profile = Profile.objects.get(user__id=user_id)

        except Profile.DoesNotExist as profile_not_found:
            detail = "You can't unfollow a profile that does not exist."
            raise NotFound(detail=detail) from profile_not_found

        requesting_profile = request.user.profile

        if not requesting_profile.has_followed(to_unfollow_profile):
            return Response(
                {"message": "You can't unfollow a user that you haven't follwoed!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        requesting_profile.unfollow(to_unfollow_profile)
        return Response(
            {
                "message": f"You have unfollowed {to_unfollow_profile.user.full_name}.",
            },
            status=status.HTTP_200_OK,
        )
