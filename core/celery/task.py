"""Celery tasks."""

import logging

from celery import shared_task
from django.core.mail import send_mail

from core.apps.articles.models import ArticleView
from core.settings import DEFAULT_FROM_EMAIL

logger = logging.getLogger(__name__)


@shared_task
def inform_followed(
    being_followed_user_first_name: str,
    to_email: str,
    user_fullname: str,
    from_email: str = DEFAULT_FROM_EMAIL,
) -> None:
    """
    Send email to the user being followed.

    Args:
       being_followed_user_first_name (str): The user being followed.
       to_email (str): The email of the user being followed.
       user_fullname (str): The user that follow the other user.
       from_email (str): The email from user that follow the other user.

    """
    mail_data = {
        "subject": "A new user follows you",
        "message": f"Hi there, {being_followed_user_first_name}! The user {user_fullname} now follows you!",
        "from_email": from_email,
        "recipient_list": [to_email],
        "fail_silently": False,
    }
    try:
        send_mail(**mail_data)
    except Exception:
        logger.exception()


@shared_task
def record_view(article_id: int, user_id: int, viewer_ip: str):
    """Record article views."""
    try:
        ArticleView.record_view(
            article_id=article_id,
            user=user_id,
            viewer_ip=viewer_ip,
        )
    except Exception:
        logger.exception()
