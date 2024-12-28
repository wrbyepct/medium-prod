"""Utililty functions for article view."""

from rest_framework.exceptions import NotFound, ValidationError

from core.apps.articles.models import Article


class ArticleUtility:
    """Article utility."""

    @staticmethod
    def get_article(article_id: str) -> Article:
        """
        Try to return an article instance by id, raise ValidationError if failed.

        Args:
            article_id (str): article id

        Raises:
            ValidationError: Article id is not proivded
            NotFound: Article does not exist.

        Returns:
            Article: Article instance.

        """
        if not article_id:
            detail = "Article id not provided. Make sure you append <aritcle_id>/ to your request url."
            raise ValidationError(detail=detail)

        try:
            return Article.objects.get(id=article_id)
        except Article.DoesNotExist as article_not_found:
            detail = "Oops, the article does not exist."
            raise NotFound(detail=detail) from article_not_found
