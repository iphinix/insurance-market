from datetime import datetime
from django.core.mail import send_mail
from .documents import ProductDocument
from elasticsearch_dsl.query import Q
from .models import Product


class SendMailService:
    @staticmethod
    def sendmail(email, subject, company):
        message = f'Уважаемая компания {company}, {datetime.now().date()} вам поступил отклик на продукт {subject}'
        return send_mail(
            subject,
            message,
            'ors3000@mail.ru',
            [email],
            fail_silently=False,
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

