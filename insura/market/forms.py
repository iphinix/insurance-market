from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from .models import Company, Product, Response


class RegisterCompanyForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class LoginCompanyForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class CompanyModelForm(ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'description', 'email']


class ProductModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.required:
            self.fields[field].required = False

    class Meta:
        model = Product
        fields = ['type', 'period', 'company', 'name']
        required = (
            'type',
            'period',
            'company',
            'name'
        )

    rate_min_field = forms.IntegerField(label='Ставка от:', required=False, widget=forms.TextInput(attrs={'class': 'form-input'}))
    rate_max_field = forms.IntegerField(label='Ставка до:', required=False, widget=forms.TextInput(attrs={'class': 'form-input'}))


class ProductModelFormES(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.required:
            self.fields[field].required = False

    class Meta:
        model = Product
        fields = ['type', 'period', 'company', 'name', 'description']
        required = (
            'type',
            'period',
            'company',
            'name',
            'description'
        )

    rate_min_field = forms.IntegerField(label='Ставка от:', required=False, widget=forms.TextInput(attrs={'class': 'form-input'}))
    rate_max_field = forms.IntegerField(label='Ставка до:', required=False, widget=forms.TextInput(attrs={'class': 'form-input'}))
    field_order = ['type', 'period', 'company', 'name', 'rate_min_field', 'rate_max_field', 'description']


class ResponseModelForm(ModelForm):
    class Meta:
        model = Response
        fields = ['name', 'email']
