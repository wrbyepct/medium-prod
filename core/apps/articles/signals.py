"""Article signals."""

# ruff: noqa: ARG001, ANN001
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django_opensearch_dsl.registries import registry

from core.apps.articles.models import Article


@receiver(post_save, sender=Article)
def update_article_document(sender, instance, created, **kwargs):
    """Update es index when new article is created or updated."""
    registry.update(instance)


@receiver(post_delete, sender=Article)
def delete_article_document(sender, instance, **kwargs):
    """Update es index when new article is deleted."""
    registry.delete(instance)
