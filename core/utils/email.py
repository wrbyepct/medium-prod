"""Utility tools."""

from django.core.mail import send_mail

from core.settings import DEFAULT_FROM_EMAIL


def inform_followed(
    follow_user_fullname: str,
    being_followed_user_first_name: str,
    being_followed_email_address: str,
) -> None:
    """
    Send email to the user being followed.

    Args:
       follow_user_fullname (str): The user that follow the other user,
       being_followed_user_first_name (str): The user being followed,
       being_followed_email_address (str): The email of the user being followed.

    """
    mail_data = {
        "subject": "A new user follows you",
        "message": f"Hi there, {being_followed_user_first_name}! The user {follow_user_fullname} now follows you!",
        "from_email": DEFAULT_FROM_EMAIL,
        "recipient_list": [being_followed_email_address],
        "fail_silently": True,
    }
    send_mail(**mail_data)
