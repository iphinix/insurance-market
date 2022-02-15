from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Product, Company


@registry.register_document
class ProductDocument(Document):
    company = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
    })

    class Index:
        name = 'products'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Product

        fields = [
            'id',
            'name',
            'type',
            'rate',
            'period',
            'description',
        ]
        related_models = [Company]

    def get_queryset(self):
        return super(ProductDocument, self).get_queryset().select_related(
            'company'
        )

    def get_instances_from_related(self, related_instance):
        return related_instance.product_set.all()
