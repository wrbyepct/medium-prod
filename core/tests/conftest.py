import pytest
from pytest_factoryboy import register

from core.tests.articles.fixtures.factories import ArticleFactory
from core.tests.user.fixtures.factories import UserFactory

register(UserFactory)
register(ArticleFactory)

pytest_plugins = [
    "core.tests.user.fixtures",
    "core.tests.fixtures",
    "core.tests.articles.fixtures",
]


def pytest_collection_modifyitems(items):
    for item in items:
        if "structure" in item.name:
            item.add_marker(pytest.mark.structure)
        if "behavior" in item.name:
            item.add_marker(pytest.mark.behavior)
        if "endpoint" in item.name:
            item.add_marker(pytest.mark.endpoint)
