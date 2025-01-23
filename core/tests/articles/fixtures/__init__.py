import pytest
from pytest_factoryboy import register

from .factories import ArticleClapFactory, ArticleFactory, ArticleViewFactory

register(ArticleFactory)
register(ArticleViewFactory)
register(ArticleClapFactory)


@pytest.fixture
def article(article_factory):
    return article_factory.create()
