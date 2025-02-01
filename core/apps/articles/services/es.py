"""Elasticsearch service."""

from django_elasticsearch_dsl import Document

from core.apps.articles.documents import ArticleDocument

ALLOWED_SEARCH_FIELDS = [
    "title",
    "description",
    "body",
    "slug",
    "author.first_name",
    "author.last_name",
    "tags",
]


def full_text_search(search_term: str, doc_cls: Document = ArticleDocument):
    """Full Search article using Elasticsearch."""
    search = doc_cls.search().query(
        "multi_match",
        query=search_term,
        fields=ALLOWED_SEARCH_FIELDS,
        fuzziness="auto",
    )
    response = search.execute()

    return [hit.id for hit in response]
