from django.core import mail

from core.tools.email import inform_followed


def test_tools__inform_followed_correct():
    mail_data = {
        "being_followed_user_first_name": "Bob",
        "to_email": "bob@example.com",
        "user_fullname": "Alice Wang",
        "from_email": "alice@example.com",
    }

    inform_followed(**mail_data)

    assert len(mail.outbox) == 1
    sent_mail = mail.outbox.pop(0)

    assert sent_mail.from_email == mail_data["from_email"]
    assert sent_mail.to == [mail_data["to_email"]]
    assert sent_mail.subject == "A new user follows you"
    assert (
        sent_mail.body
        == f"Hi there, {mail_data['being_followed_user_first_name']}! The user {mail_data['user_fullname']} now follows you!"
    )
