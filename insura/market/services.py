from datetime import datetime
from .documents import ProductDocument
from elasticsearch_dsl.query import Q
from .models import Product
from insura.tasks import send_email_task
from django.core.cache import cache


def view_count_incr(pk):
    cache.get_or_set(f"/product/{pk}", 0)
    cache.incr(f"/product/{pk}")


def zip_product_counter(company):
    products = Product.objects.filter(company_id=company.id)
    counters = []
    for prod in products:
        counters.append(cache.get(f"/product/{prod.id}"))
    return zip(products, counters)


def mail_response(product, response):

    email = product.company.email
    prod_item = product.name
    subject = f'Отклик на продукт {product.name}'
    company = product.company.name
    uname = response.name
    umail = response.email
    message = f'''Уважаемая компания {company}, вам поступил отклик на ваш продукт {prod_item}
от: {uname} с e-mail: {umail} {datetime.now().date()} числа.'''

    send_email_task.apply_async(
        (subject, message, email),
        retry=True,
        retry_policy={
            'max_retries': 10,
            'interval_start': 30,
            'interval_step': 30,
            'interval_max': 30,
        }
    )


class FilterServiceES:
    @staticmethod
    def get_queryset(request):
        query_set = ProductDocument.search().filter()
        if request.POST.get('type'):
            query_set = query_set.filter('match', type=request.POST.get('type'))
        if request.POST.get('period'):
            query_set = query_set.filter('match', period=request.POST.get('period'))
        if request.POST.get('company'):
            query_set = query_set.filter(
                            'nested',
                            path='company',
                            query=Q('match', company__id=request.POST.get('company'))
                        )
        if request.POST.get('name'):
            query_set = query_set.filter('match_phrase_prefix', name=request.POST.get('name'))
        if request.POST.get('rate_min_field'):
            query_set = query_set.filter('range', rate={'gte': request.POST.get('rate_min_field')})
        if request.POST.get('rate_max_field'):
            query_set = query_set.filter('range', rate={'lte': request.POST.get('rate_max_field')})
        if request.POST.get('description'):
            query_set = query_set.filter('match', description=request.POST.get('description'))
        return query_set


class FilterService:
    @staticmethod
    def get_queryset(request):
        query_set = Product.objects.all()
        if request.POST.get('type'):
            query_set = query_set.filter(type=request.POST.get('type'))
        if request.POST.get('period'):
            query_set = query_set.filter(period=request.POST.get('period'))
        if request.POST.get('company'):
            query_set = query_set.filter(company_id=request.POST.get('company'))
        if request.POST.get('name'):
            query_set = query_set.filter(name__contains=request.POST.get('name'))
        if request.POST.get('rate_min_field'):
            query_set = query_set.filter(rate__gte=request.POST.get('rate_min_field'))
        if request.POST.get('rate_max_field'):
            query_set = query_set.filter(rate__lte=request.POST.get('rate_max_field'))
        return query_set

