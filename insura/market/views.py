#from django.shortcuts import render, redirect
#from django.urls import reverse
from django.views.generic import View, CreateView, ListView, DetailView, UpdateView
#from django.contrib import auth
#from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from .forms import CreationCompanyForm, LoginCompanyForm, ProductModelForm

class RegisterCompany(CreateView):
    form_class = CreationCompanyForm
    template_name = 'register.html'
    success_url = 'login'


class LoginCompany(LoginView):
    form_class = LoginCompanyForm
    template_name = 'login.html'
    success_url = 'home'


class ProductList(ListView):
    form_class = ProductModelForm
    template_name = 'index.html'
    success_url = 'home'
