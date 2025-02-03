import pytest

from core.apps.articles.serializers import ArticleSerializer
from core.apps.articles.views import ArticleRetrieveUpdateDestroyView

pytestmark = pytest.mark.django_db


@pytest.mark.unit
def test_article_retrieve_view__retrieve_method_correct(article, mocker):
    view = ArticleRetrieveUpdateDestroyView()
    # Mock view.get_obeject()
    mocker.patch.object(view, "get_object", return_value=article)

    # Mock request
    mock_ip = "fake_ip"
    mock_user = article.author

    mock_request = mocker.Mock(name="fake_request")
    mock_request.META.get.return_value = mock_ip
    mock_request.user = mock_user
    view.request = mock_request  # mock for get_serializer
    view.format_kwarg = None  # mock for get_serializer

    # Mock Article.record_view
    mock_record_view = mocker.patch("core.apps.articles.views.ArticleView.record_view")

    # Act
    response = view.retrieve(request=mock_request)

    # Assert
    mock_record_view.assert_called_once_with(
        article=article, viewer_ip=mock_ip, user=mock_user
    )

    # Test return Response of serializer.data
    serializer = ArticleSerializer(article)
    assert response.data == serializer.data
