"""Response signals."""

# ruff: noqa: FBT001, ANN001, ARG001
# mypy: disable-error-code="attr-defined"
from django.db.models import F
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from core.apps.articles.models import Article

from .models import Response, ResponseClap


# Response count update
@receiver(signal=post_save, sender=Response)
def increment_reply_count(sender, instance: Response, created: bool, **kwargs):
    """Update response's reply count after a child reply is successfully created."""
    if created and instance.parent:
        Response.objects.filter(id=instance.parent_id).update(
            replies_count=F("replies_count") + 1
        )

    Article.objects.filter(id=instance.article_id).update(
        responses_count=F("responses_count") + 1
    )


@receiver(signal=post_delete, sender=Response)
def decrement_reply_count(sender, instance: Response, **kwargs):
    """Update response's reply count after a child reply is deleted."""
    if instance.parent:
        Response.objects.filter(id=instance.parent_id).update(
            replies_count=F("replies_count") - 1
        )

    Article.objects.filter(id=instance.article_id).update(
        responses_count=F("responses_count") - 1
    )


# Response clap count update
@receiver(post_save, sender=ResponseClap)
def increment_response_clap_count(sender, instance, created, **kwargs):
    """Update response's claps count after a clap is successfully created."""
    if created:
        Response.objects.filter(id=instance.response_id).update(
            claps_count=F("claps_count") + 1
        )


@receiver(post_delete, sender=ResponseClap)
def decrement_response_clap_count(sender, instance, **kwargs):
    """Update response's claps count after a clap is deleted."""
    Response.objects.filter(id=instance.response_id).update(
        claps_count=F("claps_count") - 1
    )
