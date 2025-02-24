import pytest
from faker import Faker

from core.apps.articles.services.es import full_text_search
from core.tests.articles.fixtures.documents import MockArticleDocument

pytestmark = pytest.mark.django_db

fake = Faker()


@pytest.fixture(scope="module")
def article_data():
    return {
        "title": fake.word(),
        "description": fake.word(),
        "body": fake.word(),
        "tags": [fake.word(), "b", "c"],
    }


@pytest.mark.es
def test_elasticsearch__full_text_search_article_content_correct(
    setup_article_doc_index,
    normal_user,
    article_data,
    article_factory,
):
    # Arrange: Given 3 instances with content that contain a random key word
    relevant_articles = article_factory.create_batch(
        size=3, author=normal_user, **article_data
    )
    article_data["author"] = (normal_user.first_name, normal_user.last_name)

    # Arrange: And 2 instances with content of '123'
    irrel_artcl_data = {"size": 2, "title": "123", "description": "123", "body": "123"}
    irrelevant_articles = article_factory.create_batch(**irrel_artcl_data)

    # Arrange: And register test doc with these 5 instances
    for instance in relevant_articles + irrelevant_articles:
        MockArticleDocument().update(instance)

    for field in ["title", "description", "body", "tags", "author"]:
        value = article_data[field]
        # When search through the instance by the value that relevant articles contain
        search_term = value.lower() if isinstance(value, str) else value[0]
        result_ids = full_text_search(
            search_term=search_term, doc_cls=MockArticleDocument
        )

        # Then the relevant article should be in the results
        for rel_artcl in relevant_articles:
            assert str(rel_artcl.id) in result_ids

        # And the irrelevant ones should not be in the results
        for irrel_artcl in irrelevant_articles:
            assert str(irrel_artcl.id) not in result_ids
