import pytest
from django.db import IntegrityError

from core.apps.articles.models import Clap

pytestmark = pytest.mark.django_db


# Do not create duplicate
def test_article_clap_model_behavior__do_not_create_duplicate_clap(
    article, normal_user, article_clap_factory
):
    clap = article_clap_factory.create(article=article, user=normal_user)
    assert clap.article == article
    assert clap.user == normal_user
    assert Clap.objects.all().count() == 1

    with pytest.raises(IntegrityError):
        article_clap_factory.create(article=article, user=normal_user)
