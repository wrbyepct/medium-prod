import pytest

from core.apps.articles.models import ArticleView

pytestmark = pytest.mark.django_db


def test_article_view_model__record_new_view_correct(article, normal_user, ipv4):
    assert not ArticleView.objects.filter(
        article=article, user=normal_user, viewer_ip=ipv4
    ).exists()
    ArticleView.record_view(article=article, user=normal_user, viewer_ip=ipv4)
    assert ArticleView.objects.filter(
        article=article, user=normal_user, viewer_ip=ipv4
    ).exists()


def test_article_view_model__does_not_new_record_view_if_exists(
    article, normal_user, ipv4
):
    ArticleView.record_view(article=article, user=normal_user, viewer_ip=ipv4)

    assert (
        ArticleView.objects.filter(
            article=article, user=normal_user, viewer_ip=ipv4
        ).count()
        == 1
    )

    ArticleView.record_view(article=article, user=normal_user, viewer_ip=ipv4)
    assert (
        ArticleView.objects.filter(
            article=article, user=normal_user, viewer_ip=ipv4
        ).count()
        == 1
    )
