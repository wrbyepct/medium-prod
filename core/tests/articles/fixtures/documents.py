from core.apps.articles.documents import ArticleDocument


class TestArticleDocument(ArticleDocument):
    class Index:
        name = "test_articles"
