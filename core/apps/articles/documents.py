"""Article Elasticsarch Documents."""

from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from core.apps.articles.models import Article


@registry.register_document
class ArticleDocument(Document):
    """Article Elasticsearch Document."""

    id = fields.KeywordField()
    slug = fields.TextField()
    author = fields.ObjectField(
        properties={
            "first_name": fields.TextField(),
            "last_name": fields.TextField(),
        }
    )

    tags = fields.KeywordField()

    class Index:
        name = "articles"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = Article
        fields = ["title", "body", "description"]

    def prepare_id(self, instance: Article):
        """Return article's uuid."""
        return str(instance.id)

    def prepare_tags(self, instance: Article):
        """Return tag list."""
        return [t.name for t in instance.tags.all()]
