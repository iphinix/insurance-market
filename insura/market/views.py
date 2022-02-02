from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
#from django.urls import reverse
from django.views.generic import View, CreateView, ListView, DetailView, UpdateView
#from django.contrib import auth
#from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from .forms import RegisterCompanyForm, LoginCompanyForm, ProductModelForm
from .models import Product


class RegisterCompanyView(CreateView):
    form_class = RegisterCompanyForm
    template_name = 'register.html'
    success_url = 'login'


class LoginCompanyView(LoginView):
    form_class = LoginCompanyForm
    template_name = 'login.html'
    success_url = 'home'


class ProductListView(ListView):
    #form_class = ProductModelForm
    model = Product
    template_name = 'index.html'
    success_url = 'home'


class ProductFilterView(View):
    template_name = 'index2.html'
    def get(self, request):
        #product_all = Product.objects.all()
        product_model_form = ProductModelForm()
        product_filter = Product.objects.filter()
        return render(request, self.template_name, {'products': product_filter, 'filter_form': product_model_form})
