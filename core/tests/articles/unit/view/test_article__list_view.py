import pytest
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from core.apps.articles.views import ArticleListCreateView


@pytest.mark.unit
def test_article_list_view__handle_fulltext_search__with_search_term(mocker):
    # Given a mock api request with search term
    search_term = "title=apple"
    mock_request = Request(
        APIRequestFactory().get(
            "/",
            data={"search": search_term},
        )
    )
    # And full_text_search get patched
    mock_full_text_search = mocker.patch("core.apps.articles.views.full_text_search")

    # And a view handles that requests
    view = ArticleListCreateView()
    view.request = mock_request

    # When calling handle_fulltext_search
    view.handle_fulltext_search()

    mock_full_text_search.assert_called_once_with(search_term)


@pytest.mark.unit
def test_article_list_view__handle_fulltext_search__without_search_term():
    # Given a mock API request without search term
    mock_request = Request(APIRequestFactory().get("/"))
    # And a view handles that requests
    view = ArticleListCreateView()
    view.request = mock_request

    result = view.handle_fulltext_search()

    assert result is None


@pytest.fixture
def mock_article_queryset(mocker):
    # And fake queryset
    qs = mocker.Mock(name="fake_qs")
    # And fake filtered queryset
    qs.filter.return_value = "fake_filtered_qs"
    return qs


@pytest.fixture
def article_list_view(mocker, mock_article_queryset):
    # Given view
    view = ArticleListCreateView()
    mocker.patch(
        "core.apps.articles.views.Article.statistic_objects.all",
        return_value=mock_article_queryset,
    )
    return view


class TestArticleListViewGetQueryset:
    def test_return_filterd_queryset_when_full_text_search_has_results(
        self, mocker, article_list_view, mock_article_queryset
    ):
        # Arrange: mock
        mock_full_text_search_result = [1, 2, 3]
        mocker.patch.object(
            article_list_view,
            "handle_fulltext_search",
            return_value=mock_full_text_search_result,
        )

        # Act
        result_qs = article_list_view.get_queryset()

        # Assert
        mock_article_queryset.filter.assert_called_once_with(
            id__in=mock_full_text_search_result
        )
        assert result_qs == mock_article_queryset.filter.return_value

    def test_return_base_queryset_when_full_text_search_has_no_results(
        self, mocker, article_list_view, mock_article_queryset
    ):
        # Arrange: mock
        mock_full_text_search_result = None
        mocker.patch.object(
            article_list_view,
            "handle_fulltext_search",
            return_value=mock_full_text_search_result,
        )

        # Act
        result_qs = article_list_view.get_queryset()

        # Assert
        assert result_qs == mock_article_queryset


@pytest.mark.unit
def test_article_create_view__perform_create_correct(mocker, api_request_with_user):
    # Mock setup
    request = api_request_with_user()
    mock_serializer = mocker.patch("core.apps.articles.views.ArticleSerializer")

    view = ArticleListCreateView()
    view.request = request

    # Act
    view.perform_create(mock_serializer)
    mock_serializer.save.assert_called_once_with(author=request.user)
