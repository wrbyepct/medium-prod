import pytest
import sqlparse
from django.db import connection
from django.test.utils import CaptureQueriesContext

from core.apps.bookmarks.models import ReadingCategory

pytestmark = pytest.mark.django_db


@pytest.fixture
def django_queries():
    with CaptureQueriesContext(connection) as ctx:
        yield ctx


@pytest.fixture
def categories(reading_category_factory):
    cate1 = reading_category_factory.create(with_bookmarks=1)
    cate2 = reading_category_factory.create(with_bookmarks=2)
    return cate1, cate2


# defer correct
def test_reading_category_manager__defer_correct():
    qs = ReadingCategory.objects.all()

    deferred_fields = qs.query.deferred_loading[0]

    assert "created_at" in deferred_fields


# bookmark_count in annotated field
def test_reading_category_manager__bookmark_count_in_annoted_field(categories):
    cate1, cate2 = categories
    qs = ReadingCategory.objects.all()

    cate = qs.first()
    assert hasattr(cate, "bookmarks_count")
    assert qs.get(id=cate1.id).bookmarks_count == 1
    assert qs.get(id=cate2.id).bookmarks_count == 2  # noqa: PLR2004


# prefetch make total query 2
def test_reading_category_manager__prefetch_make_only_2_query(
    categories, django_assert_num_queries, django_queries
):
    import logging

    logger = logging.getLogger(__name__)

    """
    With prefetch on Article of necessary columns:
        "id"
        "title"
        "created_at"
        "banner_image"
        "author__first_name"
        "author__last_name"

    Because no another m2m in article needed, SQL only needs to query for categories first,
    then search all articles whose cateries matching the first queries' ids.
    So in total it's 2
    """

    with django_assert_num_queries(2):
        qs = ReadingCategory.objects.all()

        for cate in qs:
            _ = list(cate.bookmarks.all())

        for q in django_queries.captured_queries:
            format_q = sqlparse.format(
                q["sql"],
                reindent=True,
                indent_with=4,
                keyword_case="upper",
            )
            logger.info(f"{format_q}\n")
