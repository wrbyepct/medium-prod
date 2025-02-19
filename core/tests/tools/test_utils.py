import pytest

from core.tests.utils.misc import get_remaining_pages


@pytest.mark.parametrize(
    "page_size, expected",
    [
        ("", 2),  # 3 - 1
        (5, 4),  # 5 - 1
        (21, 1),  # 2 - 1
    ],
)
def test_get_remaining_pages_correc(page_size, expected):
    from core.apps.articles.paginations import ArticlePagination

    paginator = ArticlePagination()

    result = get_remaining_pages(
        query_size=page_size, paginator=paginator, total_count=21
    )

    assert result == expected
