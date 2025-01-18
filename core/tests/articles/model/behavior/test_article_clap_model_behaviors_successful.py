import pytest

from core.apps.articles.models import Clap

pytestmark = pytest.mark.django_db


# Create new one successful
def test_article_clap_model_behavior__create_new_clap(article_clap_factory):
    article_clap_factory.create()

    assert article_clap_factory.article is not None
    assert article_clap_factory.user is not None
    assert Clap.objects.all().count() == 1


# string method
def test_article_clap_model_behavior__str_meothod_correct(article_clap_factory):
    clap = article_clap_factory.create()
    assert (
        clap.__str__()
        == f"User: {clap.user.first_name} clapped the article: {clap.article.title}"
    )
