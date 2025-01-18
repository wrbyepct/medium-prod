import pytest
from faker import Faker
from pytest_factoryboy import register

from .factories import ArticleClapFactory, ArticleFactory, ArticleViewFactory

register(ArticleFactory)
register(ArticleViewFactory)
register(ArticleClapFactory)

fake = Faker()


@pytest.fixture
def article(article_factory):
    return article_factory.create()


@pytest.fixture
def ipv4():
    return fake.ipv4()
