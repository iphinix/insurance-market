from django.test import TestCase, Client, RequestFactory, tag
from django.core.management import call_command
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from market import forms, models, services, views, documents


class MarketTestCase(TestCase):
    def setUp(self):
        call_command('flush', '--no-input')
        self.client = Client()
        self.factory = RequestFactory()

        self.test_user = User.objects.create_user(username='user123', password='pass123')
        self.test_company = models.Company.objects.create(name='Первая компания', user=self.test_user,
                                                          description='Описание компании', email='test123@test.ru')
        self.test_product = models.Product.objects.create(name='Автопродукт', company=self.test_company,
                                                          type='Автострахование', rate=5, period='1 год',
                                                          description='Описание продукта')
        self.test_response = models.Response.objects.create(name='Отклик', email='mail@mail.ru',
                                                            company=self.test_company, product=self.test_product)

    @tag('0')
    def test_register_company_view(self):
        url = reverse('register')
        self.assertEquals(resolve(url).func.view_class, views.RegisterCompanyView)

        response = self.client.get(url)
        self.assertTemplateUsed(response, 'register.html')
        self.assertContains(response, 'Регистрация', status_code=200, html=True)

        response = self.client.post(url, {'username': 'user456', 'password1': 'Awvrkt#2', 'password2': 'Awvrkt#2'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/company/profile/')

        response = self.client.login(username='user456', password='Awvrkt#2')
        self.assertTrue(response)

    @tag('1')
    def test_login_company_view(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func.view_class, views.LoginCompanyView)

        response = self.client.get(url)
        self.assertTemplateUsed(response, 'login.html')
        self.assertContains(response, 'Авторизация', status_code=200, html=True)

        response = self.client.post(url, {'username': 'user123', 'password': 'pass123'})
        self.assertRedirects(response, expected_url='/company/', status_code=302)

        response = self.client.get('/company/')
        self.assertEqual(str(response.context['user']), 'user123')

    @tag('2')
    def test_logout_company_view(self):
        url = reverse('logout')
        self.client.login(username='user123', password='pass123')
        self.assertEquals(resolve(url).func.view_class, views.LogoutCompanyView)

        response = self.client.get(url)
        self.assertRedirects(response, expected_url='/', status_code=302)

    @tag('3')
    def test_product_filter_view_es(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func.view_class, views.ProductFilterViewES)

        response = self.client.get(url)
        self.assertTemplateUsed(response, 'index.html')
        self.assertEqual(response.status_code, 200)

        data_true = {
            'type': 'Автострахование',
            'period': '1 год',
            'company': self.test_company,
            'name': 'имя',
            'rate_min_field': 1,
            'rate_max_field': 5,
            'description': 'описание'
        }
        data_false = {
            'type': 'Автостраховка',
            'period': '12 лет',
            'company': 'Компания',
            'name': 'имя',
            'rate_min_field': 1,
            'rate_max_field': 5,
            'description': 'описание'
        }

        form = forms.ProductModelFormES(data=data_true)
        self.assertTrue(form.is_valid())

        form = forms.ProductModelFormES(data=data_false)
        self.assertFalse(form.is_valid())

        response = self.client.post(url, {'type': 'Автострахование', 'period': '1 год'})
        self.assertContains(response, text='Первая компания', status_code=200, html=True)

    @tag('4')
    def test_product_filter_view(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'index.html')

        data_true = {
            'type': 'Автострахование',
            'period': '1 год',
            'company': self.test_company,
            'name': 'имя',
            'rate_min_field': 1,
            'rate_max_field': 5,
        }
        data_false = {
            'type': 'Автостраховка',
            'period': '12 лет',
            'company': 'Компания',
            'name': 'имя',
            'rate_min_field': 1,
            'rate_max_field': 5,
        }

        form = forms.ProductModelForm(data=data_true)
        self.assertTrue(form.is_valid())

        form = forms.ProductModelForm(data=data_false)
        self.assertFalse(form.is_valid())

        request = self.factory.get(url)
        response = views.ProductFilterView.as_view()(request)
        self.assertEqual(response.status_code, 200)

        request = self.factory.post(url, {'type': 'Автострахование', 'rate_min_field': 4})
        qs = services.FilterService().get_queryset(request)
        self.assertQuerysetEqual(qs, models.Product.objects.filter(type='Автострахование', rate=5))

    @tag('5')
    def test_product_detail_view(self):
        url = reverse('product', kwargs={'pk': 1})
        self.assertEquals(resolve(url).func.view_class, views.ProductDetailView)

        response = self.client.get(url)
        self.assertTemplateUsed(response, 'product.html')
        self.assertContains(response, text='Описание продукта', status_code=200, html=True)

        data_true = {
            'name': 'Имя',
            'email': 'mail@mail.ru'
        }

        form = forms.ResponseModelForm(data=data_true)
        self.assertTrue(form.is_valid())

        form = forms.ResponseModelForm(data={})
        self.assertFalse(form.is_valid())

        response = self.client.post(url, data_true)
        self.assertRedirects(response, expected_url='/', status_code=302)

    @tag('6')
    def test_company_home_view(self):
        url = reverse('company')
        self.assertEquals(resolve(url).func.view_class, views.CompanyHomeView)

        response = self.client.get(url)
        self.assertRedirects(response, '/login/?next=/company/', 302)

        self.client.login(username='user123', password='pass123')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'company.html')
        self.assertContains(response, text='Автопродукт', status_code=200, html=True)

    @tag('7')
    def test_company_profile(self):
        url = reverse('company_profile')
        self.client.login(username='user123', password='pass123')
        self.assertEquals(resolve(url).func.view_class, views.CompanyProfile)

        response = self.client.get(url)
        self.assertTemplateUsed(response, 'company_profile.html')
        self.assertContains(response, text='Профиль', status_code=200, html=False)

        data_true = {
            'name': 'Имя',
            'description': 'Описание',
            'email': 'mail@mail.ru'
        }

        form = forms.CompanyModelForm(data=data_true)
        self.assertTrue(form.is_valid())

        response = self.client.post(url, data_true)
        self.assertRedirects(response, expected_url='/company/', status_code=302)

    @tag('8')
    def test_company_product_add(self):
        url = reverse('company_product_add')
        self.client.login(username='user123', password='pass123')
        self.assertEquals(resolve(url).func.view_class, views.CompanyProductAdd)

        response = self.client.get(url)
        self.assertTemplateUsed(response, 'company_product_add.html')
        self.assertContains(response, text='Форма ввода нового продукта', status_code=200, html=False)

        data_true = {
            'name': 'имя',
            'type': 'Автострахование',
            'rate': 1,
            'period': '1 год',
            'description': 'описание'
        }

        form = forms.CompanyProductAddEditForm(data=data_true)
        self.assertTrue(form.is_valid())

        response = self.client.post(url, data_true)
        self.assertRedirects(response, expected_url='/company/', status_code=302)

    @tag('9')
    def test_company_product_edit(self):
        url = reverse('company_product_edit', kwargs={'pk': 1})
        self.client.login(username='user123', password='pass123')
        self.assertEquals(resolve(url).func.view_class, views.CompanyProductEdit)

        response = self.client.get(url)
        self.assertTemplateUsed(response, 'company_product_edit.html')
        self.assertContains(response, text='Форма редактирования продукта', status_code=200, html=False)

        data_true = {
            'name': 'имя',
            'type': 'Автострахование',
            'rate': 1,
            'period': '1 год',
            'description': 'описание'
        }

        form = forms.CompanyProductAddEditForm(data=data_true)
        self.assertTrue(form.is_valid())

        response = self.client.post(url, data_true)
        self.assertRedirects(response, expected_url='/company/', status_code=302)

    @tag('10')
    def test_company_product_delete(self):
        url = reverse('company_product_delete', kwargs={'pk': 1})
        self.client.login(username='user123', password='pass123')
        self.assertEquals(resolve(url).func.view_class, views.CompanyProductDelete)

        response = self.client.post(url)
        self.assertRedirects(response, expected_url='/company/', status_code=302)

    @tag('11')
    def test_company_response_view(self):
        url = reverse('company_response')
        self.client.login(username='user123', password='pass123')
        self.assertEquals(resolve(url).func.view_class, views.CompanyResponseView)

        response = self.client.get(url)
        self.assertTemplateUsed(response, 'company_response.html')
        self.assertContains(response, text='mail@mail.ru', status_code=200, html=False)

        request = self.factory.get(url)
        request.user = self.test_user
        view = views.CompanyResponseView()
        view.request = request
        qs = view.get_queryset()
        self.assertQuerysetEqual(qs, models.Response.objects.filter(company__user__id=request.user.id))
