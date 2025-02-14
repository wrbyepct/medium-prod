import pytest
from faker import Faker

from core.apps.articles.services.es import full_text_search
from core.tests.articles.fixtures.documents import TestArticleDocument

pytestmark = pytest.mark.django_db

fake = Faker()


@pytest.fixture(scope="module")
def article_data():
    return {
        "title": fake.word(),
        "description": fake.word(),
        "body": fake.word(),
        "tags": [fake.word(), "b", "c"],
        "author": (fake.first_name(), fake.last_name()),
    }


@pytest.fixture
def prepare_relevant_articles(
    article_factory,
    user_factory,
):
    # create 3 article instances that use searching word
    def _create(field, value):
        if field == "author":
            user_info = {"first_name": value[0], "last_name": value[1]}
            user = user_factory(**user_info)
            rel_artcl_data = {"size": 3, field: user}
        else:
            rel_artcl_data = {"size": 3, field: value}

        return article_factory.create_batch(**rel_artcl_data)

    return _create


@pytest.mark.es
@pytest.mark.parametrize(
    "field",
    ["title", "description", "body", "tags", "author"],
)
def test_elasticsearch__full_text_search_article_content_correct(
    setup_article_doc_index,
    field,
    article_data,
    prepare_relevant_articles,
    article_factory,
):
    # Given 3 instances with content that contain a random key word
    value = article_data[field]
    relevant_articles = prepare_relevant_articles(field=field, value=value)

    # And 2 instances with content of '123'
    irrel_artcl_data = {"size": 2, "title": "123", "description": "123", "body": "123"}
    irrelevatn_articles = article_factory.create_batch(**irrel_artcl_data)

    # And register test doc with these 5 instances
    for instance in relevant_articles + irrelevatn_articles:
        TestArticleDocument().update(instance)

    # When search through the instance by the value that relevant articles contain
    search_term = value.lower() if isinstance(value, str) else value[0]
    result_ids = full_text_search(search_term=search_term, doc_cls=TestArticleDocument)

    # Then the relevant article should be in the results
    for rel_artcl in relevant_articles:
        assert str(rel_artcl.id) in result_ids

    # And teh irrelevant ones should not be in the results
    for irrel_artcl in irrelevatn_articles:
        assert str(irrel_artcl.id) not in result_ids
