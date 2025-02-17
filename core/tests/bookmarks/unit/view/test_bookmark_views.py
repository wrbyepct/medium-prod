from unittest.mock import call

import pytest
from django.http import Http404
from django_mock_queries.mocks import MockSet

from core.apps.articles.models import Article
from core.apps.bookmarks.models import ReadingCategory
from core.apps.bookmarks.views import (
    BookmarkCategoryCreateView,
    BookmarkCategoryListView,
    BookmarkDestoryView,
)

pytestmark = pytest.mark.django_db


# category list view qs returns
def test_category_list_view__get_qs_return_user_categories_only(
    reading_category_factory, normal_user, mocker
):
    # Arrange: given 3 normal user's categories and 2 not belong to normal user
    user_cates_num = 3
    user_cates = reading_category_factory.build_batch(
        size=user_cates_num, user=normal_user
    )
    non_user_cates = reading_category_factory.build_batch(size=2)

    # Arrange: Mock view's request and queryset
    view = BookmarkCategoryListView()
    view.request = mocker.Mock(user=normal_user)
    view.queryset = MockSet(
        *(user_cates + non_user_cates)
    )  # MockSet take instances individually

    # Act
    result_qs = view.get_queryset()

    assert len(result_qs) == user_cates_num
    for cate in result_qs:
        assert cate in user_cates
        assert cate not in non_user_cates

    result_qs.order_by("-is_reading_list", "-updated_at")
    for result_cate, user_cate in zip(result_qs, user_cates):
        assert result_cate == user_cate


# category create view set "article_id" to context
def test_category_create_view__set_article_id_to_serializer_ocntext(mocker):
    # Arrange: mock request with query_params containing articl_id

    request = mocker.Mock()
    params = {"article_id": "some_id"}
    request.query_params = params

    # Arrange: given category create view
    view = BookmarkCategoryCreateView()
    view.request = request
    view.format_kwarg = "stub"

    # Act
    context = view.get_serializer_context()

    assert "article_id" in context
    assert context["article_id"] == params["article_id"]


# category create view -- perform_create call serializer.save(user=self.request.user)
def test_category_create_view__perform_create_call_serializer_save_method_correct(
    mocker,
):
    # Mock request
    stub_user = "stub user"

    request = mocker.Mock(user=stub_user)
    view = BookmarkCategoryCreateView()
    view.request = request

    # Mock serializer
    mock_serializer = mocker.Mock()

    # Act
    view.perform_create(mock_serializer)

    # Assert
    mock_serializer.save.assert_called_once_with(user=stub_user)


# test destroy view delete side effect called correctly


def test_category_destory_view__side_effects_called_correct(mocker):
    mock_article = mocker.Mock(id="stub_id")
    mock_category = mocker.Mock()

    # Arrange: mocok get_object_or_404 in delete method
    mock_go404 = mocker.patch(
        "core.apps.bookmarks.views.get_object_or_404",
        side_effect=[mock_article, mock_category],
    )
    # Arrange: prepare dummy params for delete method
    stub_user = "stub_user"
    stub_slug = "stub_slug"
    request = mocker.Mock(user=stub_user)

    # Act
    view = BookmarkDestoryView()
    view.delete(request=request, slug=stub_slug, article_id=mock_article.id)

    # Assert
    expected_call_times = 2
    assert mock_go404.call_count == expected_call_times
    mock_go404.assert_has_calls(
        [
            call(Article, id=mock_article.id),
            call(ReadingCategory, user=stub_user, slug=stub_slug),
        ],
        any_order=True,
    )
    mock_category.bookmarks.remove.assert_called_once_with(mock_article)


def test_category_destory_view__any_object_not_found_raise_http404(mocker):
    mock_go404 = mocker.patch(
        "core.apps.bookmarks.views.get_object_or_404", side_effect=[Http404]
    )

    stub_id = "stub_id"
    view = BookmarkDestoryView()
    with pytest.raises(Http404):
        view.delete(request="stub_request", slug="stub_slug", article_id=stub_id)

    mock_go404.assert_called_once_with(Article, id=stub_id)
