from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import View, CreateView, ListView, DetailView, UpdateView
from django.contrib import auth
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import LoginView, LogoutView
from .forms import RegisterCompanyForm, LoginCompanyForm, ProductModelForm, ResponseModelForm, CompanyModelForm
from .models import Company, Product, Response, User


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


class ProductFilterView(View):
    template_name = 'index.html'

    def get(self, request):
        product_model_form = ProductModelForm()
        product_filter = Product.objects.all()
        return render(request, self.template_name, {'products': product_filter, 'filter_form': product_model_form})

    def post(self, request):
        voc = {}
        product_model_form = ProductModelForm(request.POST)
        if product_model_form.is_valid():
            if product_model_form.cleaned_data['type']:
                voc['type'] = product_model_form.cleaned_data['type']
            if product_model_form.cleaned_data['period']:
                voc['period'] = product_model_form.cleaned_data['period']
            if product_model_form.cleaned_data['company']:
                voc['company'] = product_model_form.cleaned_data['company']
            if product_model_form.cleaned_data['name']:
                voc['name__contains'] = product_model_form.cleaned_data['name']
            if product_model_form.cleaned_data['rate_min_field']:
                voc['rate__gte'] = product_model_form.cleaned_data['rate_min_field']
            if product_model_form.cleaned_data['rate_max_field']:
                voc['rate__lte'] = product_model_form.cleaned_data['rate_max_field']
            product_filter = Product.objects.filter(**voc)
            return render(request, self.template_name, {'products': product_filter, 'filter_form': product_model_form})


class ProductDetailView(View):
    template_name = 'product.html'

    def get(self, request, *args, **kwargs):
        product = Product.objects.get(pk=kwargs['pk'])
        response_model_form = ResponseModelForm()
        return render(request, self.template_name, {'product': product, 'response_form': response_model_form})

    def post(self, request, *args, **kwargs):
        product = Product.objects.get(pk=kwargs['pk'])
        response = Response()
        response.name = request.POST['name']
        response.email = request.POST['email']
        response.company_id = product.company_id
        response.product_id = product.pk
        response.save()
        return redirect('home')


class CompanyHomeView(View):
    template_name = 'company.html'

    def get(self, request, *args, **kwargs):
        company = Company.objects.get(user_id=request.user.id)
        return render(request, self.template_name, {'company': company})

    def post(self, request, *args, **kwargs):
        company = Company.objects.get(user_id=request.user.id)
        company.name = request.POST['name']
        company.description = request.POST['description']
        company.save()
        return render(request, self.template_name, {'company': company})
