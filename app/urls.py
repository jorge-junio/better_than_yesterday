from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('', views.home, name="home"),

    path('', include('brands.urls')),
    path('', include('categories.urls')),
    path('', include('customers.urls')),
    path('', include('inflows.urls')),
    path('', include('outflows.urls')),
    path('', include('payables.urls')),
    path('', include('products.urls')),
    path('', include('receivables.urls')),
    path('', include('sales.urls')),
    path('', include('suppliers.urls')),
]
