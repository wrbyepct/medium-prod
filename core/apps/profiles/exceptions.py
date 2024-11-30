"""Custom exception."""

from rest_framework.exceptions import APIException


class CantFollowYourselfException(APIException):
    """Custom exception for Profile business logic."""

    status_code = 403
    default_detail = "You cannot follow yourself."
    default_code = "forbidden"
