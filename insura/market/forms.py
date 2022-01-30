from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from .models import Company, Product, Response


class CreationCompanyForm(UserCreationForm):
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
        fields = '__all__'


class ResponseModelForm(ModelForm):
    class Meta:
        model = Response
        fields = '__all__'
