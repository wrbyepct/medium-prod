import pytest

from core.apps.articles.serializers import TagListField


def test_article_serializer__taglist_field_deserialize_correct():
    tags = '["   A", "B", "C   ", ""]'

    tags = TagListField().to_internal_value(data=tags)
    assert tags == ["A", "B", "C"]


@pytest.mark.parametrize(
    "invalid_tags",
    [
        "1",  # Not stringified list
        "[1, 2, 3]",  # Not stringified list of string type elements
        "[1, 2, '3']",  # 1 of them is not stringified list of string type elements
        [1, 2, 3],  # Not string
        "@F2323{}",  # Cannot be converted to JSON
    ],
)
def test_article_serializer__taglist_field_deserialize_capture_invalid_data(
    invalid_tags,
):
    from rest_framework.serializers import ValidationError

    with pytest.raises(ValidationError) as e:
        TagListField().to_internal_value(data=invalid_tags)
        assert e == """Expected a string of list of tags.\n E.g., '["tag1", "tag2"]'"""
