from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from .models import Company, Product, Response


class RegisterCompanyForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'frm-ctl-lg'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'frm-ctl-lg'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'frm-ctl-lg'}))


class LoginCompanyForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'autofocus': True, 'class': 'frm-ctl-lg'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'frm-ctl-lg'}))


class CompanyModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.fields:
            self.fields[field].widget.attrs['class'] = 'frm-ctl'
        self.fields['description'].widget.attrs['class'] = 'frm-ctl-d'

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

    rate_min_field = forms.IntegerField(label='Ставка от:', required=False, widget=forms.TextInput())
    rate_max_field = forms.IntegerField(label='Ставка до:', required=False, widget=forms.TextInput())


class ProductModelFormES(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.required:
            self.fields[field].required = False
            self.fields[field].widget.attrs['class'] = 'frm-ctl'
        self.fields['description'].widget.attrs['class'] = 'frm-ctl-d'

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

    rate_min_field = forms.IntegerField(label='Ставка от:', required=False, widget=forms.NumberInput(attrs={'class': 'frm-ctl'}))
    rate_max_field = forms.IntegerField(label='Ставка до:', required=False, widget=forms.NumberInput(attrs={'class': 'frm-ctl'}))
    field_order = ['type', 'period', 'company', 'name', 'rate_min_field', 'rate_max_field', 'description']


class ResponseModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'frm-ctl-lg'
        self.fields['email'].widget.attrs['class'] = 'frm-ctl-lg'

    class Meta:
        model = Response
        fields = ['name', 'email']


class CompanyProductAddEditForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.fields:
            self.fields[field].widget.attrs['class'] = 'frm-ctl'
        self.fields['description'].widget.attrs['class'] = 'frm-ctl-d'

    class Meta:
        model = Product
        fields = ['name', 'type', 'rate', 'period', 'description']
