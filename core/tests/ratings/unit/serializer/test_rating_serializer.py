import pytest

from core.apps.ratings.serializers import RatingSerializer

pytestmark = pytest.mark.django_db


# test deserilaize correct data -> obj
def test_rating_serializer__deserialize_correct(normal_user, article):
    data = {"rating": 1, "review": "It's not bad"}

    serializer = RatingSerializer(data=data)
    assert serializer.is_valid()

    for key in data:
        assert key in serializer.validated_data

    rating = serializer.save(user=normal_user, article=article)

    assert rating.rating == data["rating"]
    assert rating.review == data["review"]
    assert rating.user == normal_user
    assert rating.article == article


# test serialize correct correct: obj -> data
def test_rating_serializer__serialize_correct(rating_factory, normal_user, article):
    rating = rating_factory(user=normal_user, article=article)

    serializer = RatingSerializer(rating)

    fields = RatingSerializer.Meta.fields
    for field in fields:
        assert field in serializer.data

    data = serializer.data
    assert data["id"] == str(rating.id)
    assert data["rating"] == rating.rating
    assert data["review"] == rating.review
    assert data["article_title"] == article.title
    assert data["user_full_name"] == normal_user.full_name


@pytest.mark.ccc
@pytest.mark.parametrize(
    "invalid_data",
    ["test", -1, None],
)
def test_rating_serializer__deserialize_with_invalid_rating_raise_error(invalid_data):
    invalid_data = {"rating": invalid_data}

    serializer = RatingSerializer(data=invalid_data)

    assert not serializer.is_valid()


@pytest.mark.parametrize(
    "invalid_data",
    [
        [1, 2, 3],
        {"2", "4", "3"},
        -1,
    ],
)
def test_rating_serializer__deserialize_with_invalid_review_raise_error(invalid_data):
    invalid_data = {"review": invalid_data}

    serializer = RatingSerializer(data=invalid_data)

    assert not serializer.is_valid()


# test read only fields do not show in validated data
def test_rating_serializer__read_only_fields_do_not_show_in_validated_data():
    data = {
        "rating": 1,
        "review": "It's not bad",
        "id": 1234,
        "article_title": "Test",
        "user_full_name": "Test User",
    }

    serializer = RatingSerializer(data=data)

    assert serializer.is_valid()

    read_only_fields = ["id", "article_title", "user_full_name"]

    for field in read_only_fields:
        assert field not in serializer.validated_data


# test serializer method correct
def test_rating_serializer__serializer_method_correct(rating_factory):
    rating = rating_factory.create()
    user = rating.user

    user_full_name = RatingSerializer().get_user_full_name(rating)
    assert user_full_name == user.full_name
