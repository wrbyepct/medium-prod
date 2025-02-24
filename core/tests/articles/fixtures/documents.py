from core.apps.articles.documents import ArticleDocument


class MockArticleDocument(ArticleDocument):
    class Index:
        name = "test_articles"
