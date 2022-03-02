"""insura URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from market import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.ProductFilterViewES.as_view(), name='home'),
    path('product/<int:pk>', views.ProductDetailView.as_view(), name='product'),
    path('register/', views.RegisterCompanyView.as_view(), name='register'),
    path('login/', views.LoginCompanyView.as_view(), name='login'),
    path('logout/', views.LogoutCompanyView.as_view(), name='logout'),
    path('company/', views.CompanyHomeView.as_view(), name='company'),
    path('company/profile/', views.CompanyProfile.as_view(), name='company_profile'),
    path('company/product/add', views.CompanyProductAdd.as_view(), name='company_product_add'),
    path('company/product/edit/<int:pk>', views.CompanyProductEdit.as_view(), name='company_product_edit'),
    path('company/product/delete/<int:pk>', views.CompanyProductDelete.as_view(), name='company_product_delete'),
    path('company/response/', views.CompanyResponseView.as_view(), name='company_response'),
]
