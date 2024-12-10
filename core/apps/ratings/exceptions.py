"""Rating exceptions."""

from rest_framework.exceptions import APIException


class YouCannotRateArticleAgain(APIException):
    """Custom Exception: Cannot rate the same article again."""

    status_code = 400
    default_detail = "You have already rated this article."
    default_code = "bad_request"
