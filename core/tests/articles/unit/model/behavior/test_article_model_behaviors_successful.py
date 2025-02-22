import pytest
from django.utils.text import slugify

pytestmark = pytest.mark.django_db


def test_article_model_behavior__create_article_successful(
    mock_article_index_update,
    mock_media_dir,
    normal_user,
    article_factory,
):
    article = article_factory.create(
        author=normal_user, tags=["a", "b"], with_image=True
    )

    assert article.title is not None
    assert article.description is not None
    assert article.body is not None
    assert article.banner_image.name.startswith("uploads/articles/")
    assert article.author == normal_user
    assert list(article.tags.names()) == ["a", "b"]

    slug_prefix = slugify(article.title)

    assert article.slug.startswith(slug_prefix)


def test_article_model_behavior__slug_is_unique(article_factory):
    title = "Test Title"
    article_1 = article_factory(title=title)
    article_2 = article_factory(title=title)

    assert article_1.slug != article_2.slug


def test_article_model_behavior__str_method(article_factory, normal_user):
    article = article_factory.create(author=normal_user)
    assert article.__str__() == f"{article.author}'s article | {article.title}"
