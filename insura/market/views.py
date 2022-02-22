from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import View, CreateView, ListView, DetailView, UpdateView
from django.contrib import auth
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import LoginView, LogoutView
from .forms import RegisterCompanyForm, LoginCompanyForm, ProductModelForm, ProductModelFormES, ResponseModelForm, CompanyModelForm
from .models import Company, Product, Response, User
from .documents import ProductDocument
from elasticsearch_dsl.query import Q
from insura.tasks import send_email_task
from django.utils import timezone
from datetime import datetime


class RegisterCompanyView(CreateView):
    form_class = RegisterCompanyForm
    template_name = 'register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginCompanyView(LoginView):
    form_class = LoginCompanyForm
    template_name = 'login.html'


class LogoutCompanyView(View):
    def get(self, *args, **kwargs):
        logout(self.request)
        return redirect('home')


class ProductListView(ListView):
    model = Product
    template_name = 'index0.html'
    success_url = 'home'

    def get_queryset(self):
        qs = Product.objects.filter()
        return qs


class ProductFilterView(View):
    template_name = 'index.html'

    def get_queryset(self, request):
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

    def get(self, request):
        product_model_form = ProductModelForm()
        product_filter = self.get_queryset(request)
        return render(request, self.template_name, {'products': product_filter, 'filter_form': product_model_form})

    def post(self, request):
        product_model_form = ProductModelForm(request.POST)
        product_filter = self.get_queryset(request)
        return render(request, self.template_name, {'products': product_filter, 'filter_form': product_model_form})


class ProductFilterViewES(View):
    template_name = 'index.html'

    def get_queryset(self, request):
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

    def get(self, request):
        #print('ДатаВремя', datetime.now(), 'ТаймЗоне', timezone.now())
        product_model_form = ProductModelFormES()
        product_filter = self.get_queryset(request)
        return render(request, self.template_name, {'products': product_filter, 'filter_form': product_model_form})

    def post(self, request):
        product_model_form = ProductModelFormES(request.POST)
        product_filter = self.get_queryset(request)
        return render(request, self.template_name, {'products': product_filter, 'filter_form': product_model_form})


class ProductDetailView(View):
    template_name = 'product.html'

    def get(self, request, *args, **kwargs):
        product = Product.objects.get(pk=kwargs['pk'])
        response_model_form = ResponseModelForm()
        return render(request, self.template_name, {'product': product, 'response_form': response_model_form})

    def post(self, request, *args, **kwargs):
        product = Product.objects.get(pk=kwargs['pk'])
        response_model_form = ResponseModelForm(request.POST)
        response = response_model_form.save(commit=False)
        response.company_id = product.company_id
        response.product_id = product.pk
        response.save()
        email = product.company.email
        subject = product.name
        message = f'Уважаемая компания {product.company.name}, {datetime.now()} вам поступил отклик на продукт {product.name}'
        send_email_task.delay(email, subject, message)
        return redirect('home')


class CompanyHomeView(View):
    template_name = 'company.html'

    def get(self, request, *args, **kwargs):
        company = Company.objects.get(user_id=request.user.id)
        company_model_form = CompanyModelForm(instance=company)
        return render(request, self.template_name, {'company': company, 'company_form': company_model_form})

    def post(self, request, *args, **kwargs):
        company = Company.objects.get(user_id=request.user.id)
        company_model_form = CompanyModelForm(request.POST, instance=company)
        company_model_form.save()
        return render(request, self.template_name, {'company': company, 'company_form': company_model_form})
