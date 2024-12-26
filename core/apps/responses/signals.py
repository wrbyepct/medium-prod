"""Response signals."""

# ruff: noqa: FBT001, ANN001, ARG001
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Response, ResponseClap


# Response count update
@receiver(signal=post_save, sender=Response)
def increment_reply_count(sender, instance: Response, created: bool, **kwargs):
    """Update response's reply count after a child reply is successfully created."""
    if created and instance.parent:
        instance.parent.replies_count += 1
        instance.parent.save()
    instance.article.responses_count += 1
    instance.article.save()


@receiver(signal=post_delete, sender=Response)
def decrement_reply_count(sender, instance: Response, **kwargs):
    """Update response's reply count after a child reply is deleted."""
    if instance.parent:
        instance.parent.replies_count -= 1
        instance.parent.save()
    instance.article.responses_count += 1
    instance.article.save()


# Response clap count update
@receiver(post_save, sender=ResponseClap)
def increment_response_clap_count(sender, instance, created, **kwargs):
    """Update response's claps count after a clap is successfully created."""
    if created:
        instance.response.claps_count += 1
        instance.response.save()


@receiver(post_delete, sender=ResponseClap)
def decrement_response_clap_count(sender, instance, created, **kwargs):
    """Update response's claps count after a clap is deleted."""
    instance.response.claps_count -= 1
    instance.response.save()
