"""Profile views."""

from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from core.utils.email import inform_followed

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

        So you don't query every through profile for user.
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


class FollowersListAPIView(APIView):
    """
    Follower API view.

    Rewrite '.get()':
        return followers_count and followers data.
    """

    def get(self, request, format=None):
        """Return Response containing followers_count and followers data."""
        try:
            profile = Profile.objects.get(user=request.user)

        except Profile.DoesNotExist:
            return Response(status=404)

        followers = profile.followers.all()
        serializer = FollowingSerializer(followers, many=True)

        formatted_response = {
            "followers_count": followers.count(),
            "followers": serializer.data,
        }
        return Response(formatted_response)


class FollowingAPIView(APIView):
    """Get following user view."""

    def get(self, request, user_id, format=None, *args, **kwargs):
        """Get a list of follwing users."""
        try:
            profile = Profile.objects.get(user__id=user_id)

        except Profile.DoesNotExist:
            return Response(status=404)

        following_profiles = profile.following.all()

        serializer = FollowingSerializer(following_profiles, many=True)
        formatted_response = {
            "following_count": following_profiles.count(),
            "followings": serializer.data,
        }
        return Response(formatted_response)


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
            "follow_user_fullname": requesting_profile.user.full_name,
            "being_followed_user_first_name": to_follow_profile.user.first_name,
            "being_followed_email_address": to_follow_profile.user.email,
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
                "statud_code": 200,
                "message": f"You have unfollowed {to_unfollow_profile.user.full_name}.",
            },
            status=status.HTTP_200_OK,
        )
