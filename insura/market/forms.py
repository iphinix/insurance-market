from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from .models import Company, Product, Response


class RegisterCompanyForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class LoginCompanyForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')


class CompanyModelForm(ModelForm):
    class Meta:
        model = Company
        fields = '__all__'


class ProductModelForm(ModelForm):
    class Meta:
        model = Product
        fields = ['type']
    #type_field = forms.ChoiceField(choices=Product.TYPE_CHOICES)


class ResponseModelForm(ModelForm):
    class Meta:
        model = Response
        fields = '__all__'
