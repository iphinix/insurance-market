from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.views.generic import View, CreateView, ListView, DetailView, UpdateView
from django.contrib import auth
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import LoginView, LogoutView
from .forms import (RegisterCompanyForm, LoginCompanyForm, ProductModelForm,
                    ProductModelFormES, ResponseModelForm, CompanyModelForm,
                    CompanyProductAddEditForm)
from .models import Company, Product, Response, User
from insura.tasks import send_email_task
import redis
from insura.settings import REDIS_HOST
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .services import FilterServiceES, FilterService


r_products = redis.Redis(host=REDIS_HOST, decode_responses=True)


class RegisterCompanyView(CreateView):
    form_class = RegisterCompanyForm
    template_name = 'register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        Company.objects.create(name='Компания-'+str(self.request.user.id), user_id=self.request.user.id)
        return redirect('company_profile')


class LoginCompanyView(LoginView):
    form_class = LoginCompanyForm
    template_name = 'login.html'


class LogoutCompanyView(View):
    def get(self, *args, **kwargs):
        logout(self.request)
        return redirect('home')


class ProductFilterView(View):
    template_name = 'index.html'

    def get(self, request):
        product_model_form = ProductModelForm()
        product_filter = FilterService.get_queryset(request)
        return render(request, self.template_name, {'products': product_filter, 'filter_form': product_model_form})

    def post(self, request):
        product_model_form = ProductModelForm(request.POST)
        product_filter = FilterService.get_queryset(request)
        return render(request, self.template_name, {'products': product_filter, 'filter_form': product_model_form})


class ProductFilterViewES(View):
    template_name = 'index.html'

    def get(self, request):
        product_model_form = ProductModelFormES()
        product_filter = FilterServiceES.get_queryset(request)
        return render(request, self.template_name, {'products': product_filter, 'filter_form': product_model_form})

    def post(self, request):
        product_model_form = ProductModelFormES(request.POST)
        product_filter = FilterServiceES.get_queryset(request)
        return render(request, self.template_name, {'products': product_filter, 'filter_form': product_model_form})


class ProductDetailView(View):
    template_name = 'product.html'

    def get(self, request, *args, **kwargs):
        product = Product.objects.get(pk=kwargs['pk'])
        response_model_form = ResponseModelForm()
        counter = r_products.get(f"/product/{kwargs['pk']}")
        if not counter:
            counter = 0
        r_products.set(f"/product/{kwargs['pk']}", int(counter)+1)
        return render(request, self.template_name, {'product': product, 'response_form': response_model_form})

    def post(self, request, *args, **kwargs):
        product = Product.objects.get(pk=kwargs['pk'])
        response_model_form = ResponseModelForm(request.POST)
        response = response_model_form.save(commit=False)
        response.company_id = product.company_id
        response.product_id = product.pk
        response.save()
        uname = request.POST.get('name')
        umail = request.POST.get('email')
        email = product.company.email
        subject = product.name
        company = product.company.name
        send_email_task.apply_async(
            (email, subject, company, uname, umail),
            retry=True,
            retry_policy={
                'max_retries': 10,
                'interval_start': 30,
                'interval_step': 30,
                'interval_max': 30,
            }
        )
        return redirect('home')


@method_decorator(login_required, name='dispatch')
class CompanyHomeView(View):
    template_name = 'company.html'

    def get(self, request, *args, **kwargs):
        company = Company.objects.get(user_id=request.user.id)
        products = Product.objects.filter(company_id=company.id)
        counters = []
        for prod in products:
            counters.append(r_products.get(f"/product/{prod.id}"))
        return render(request, self.template_name, {'company': company, 'prod_count': zip(products, counters)})


@method_decorator(login_required, name='dispatch')
class CompanyProfile(View):
    template_name = 'company_profile.html'

    def get(self, request, *args, **kwargs):
        company = Company.objects.get(user_id=request.user.id)
        company_model_form = CompanyModelForm(instance=company)
        return render(request, self.template_name, {'company': company, 'company_form': company_model_form})

    def post(self, request, *args, **kwargs):
        company = Company.objects.get(user_id=request.user.id)
        company_model_form = CompanyModelForm(request.POST, instance=company)
        company_model_form.save()
        return redirect('company')


@method_decorator(login_required, name='dispatch')
class CompanyProductAdd(View):
    template_name = 'company_product_add.html'

    def get(self, request):
        company_product_add_form = CompanyProductAddEditForm()
        return render(request, self.template_name, {'form': company_product_add_form})

    def post(self, request):
        company_product_add_form = CompanyProductAddEditForm(request.POST)
        product_add = company_product_add_form.save(commit=False)
        product_add.company_id = Company.objects.get(user_id=request.user.id).id
        product_add.save()
        return redirect('company')


@method_decorator(login_required, name='dispatch')
class CompanyProductEdit(View):
    template_name = 'company_product_edit.html'

    def get(self, request, *args, **kwargs):
        company_product = Product.objects.get(pk=kwargs['pk'])
        company_product_edit_form = CompanyProductAddEditForm(instance=company_product)
        return render(request, self.template_name, {'company_product': company_product, 'form': company_product_edit_form})

    def post(self, request, *args, **kwargs):
        company_product = Product.objects.get(pk=kwargs['pk'])
        company_product_edit_form = CompanyProductAddEditForm(request.POST, instance=company_product)
        company_product_edit_form.save()
        return redirect('company')


@method_decorator(login_required, name='dispatch')
class CompanyProductDelete(View):
    def post(self, request, *args, **kwargs):
        Product.objects.get(pk=kwargs['pk']).delete()
        r_products.delete(f"/product/{kwargs['pk']}")
        return redirect('company')


@method_decorator(login_required, name='dispatch')
class CompanyResponseView(ListView):
    model = Response
    template_name = 'company_response.html'

    def get_queryset(self):
        query_set = Response.objects.filter(company__user__id=self.request.user.id)
        return query_set
