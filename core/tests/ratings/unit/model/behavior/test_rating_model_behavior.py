import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from core.apps.articles.models import Article
from core.apps.ratings.models import Rating

User = get_user_model()

pytestmark = pytest.mark.django_db
# test model create correct


def test_rating_model_behavior__create_successful_and_data_correct(rating_factory):
    rating = rating_factory.create()

    assert rating.user is not None
    assert isinstance(rating.user, User)

    assert rating.article is not None
    assert isinstance(rating.article, Article)

    assert rating.rating in [value for value, _ in Rating.RATING_CHOICES]
    assert rating.review is not None
    assert isinstance(rating.review, str)


def test_rating_model_behavior__str_method_correct(rating_factory):
    rating = rating_factory.create()
    user = rating.user
    article = rating.article

    assert (
        rating.__str__()
        == f"Article:{article.title} rated: {rating.rating} by user: {user.full_name}"
    )


# test model create fail cases
# rating: negative integer, non integer
@pytest.mark.parametrize(
    "value, expected_error",
    [
        ("test", ValueError),
        (-1, IntegrityError),
    ],
)
def test_rating_model_behavior__create_with_invalid_rating_raise_errors(
    rating_factory, value, expected_error
):
    with pytest.raises(expected_error):
        rating_factory.create(rating=value)


# test remote model behave correct
@pytest.mark.parametrize("remote_model", ["user", "article"])
def test_rating_model_behavior__remote_instance_delete_cascade(
    rating_factory, remote_model
):
    rating = rating_factory.create()
    rating_id = rating.id
    assert Rating.objects.filter(id=rating_id).exists()

    remote_instance = getattr(rating, remote_model)
    remote_instance.delete()

    assert not Rating.objects.filter(id=rating_id).exists()


# missing mandatory fields
@pytest.mark.parametrize(
    "mandatory_field",
    [
        {"user": None},
        {"article": None},
        {"rating": None},
    ],
)
def test_rating_model_behavior__create_missing_mandatory_field_raise_errors(
    rating_factory, mandatory_field
):
    with pytest.raises(IntegrityError):
        rating_factory.create(**mandatory_field)
