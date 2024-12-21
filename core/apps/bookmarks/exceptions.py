"""Bookmark exceptions."""

from rest_framework.exceptions import APIException


class YouCannotBookmarkAgain(APIException):
    """Custom API exception, you cannot bookmark the same article."""

    status_code = 400
    default_code = "bad_request"
    default_detail = "You already bookmarked the same article."
