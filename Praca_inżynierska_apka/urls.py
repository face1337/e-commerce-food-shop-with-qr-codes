"""Praca_inżynierska_apka URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.urls import include, path

from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView

from users import views as user_views
from orders import views as order_views


urlpatterns = [
    path('admin/', admin.site.urls),

    path('register/', user_views.RegisterView.as_view(), name='users-register'),

    path('login/', user_views.MyLoginView.as_view(template_name='users/login.html'), name='users-login'),

    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='users-logout'),

    path('address/',user_views.AddressListView.as_view(), name='users-address_list'),

    path('address/create', user_views.AddressCreateView.as_view(), name='users-address_create'),

    path('address/<int:pk>/update', user_views.AddressUpdateView.as_view(), name='users-address_update'),

    path('address/<int:pk>/delete', user_views.AddressDeleteView.as_view(), name='users-address_confirm_delete'),

    path('add_to_cart/', order_views.add_to_cart, name='orders-add_to_cart'),

    path('cart/', order_views.manage_cart, name='orders-cart'),

    path('orders/address_select', user_views.AddressSelectView.as_view(), name='users-address_select'),

    path('orders/checkout', TemplateView.as_view(template_name="orders/order_done.html"), name='orders-order_done'),

    path('orders/<str:email>', user_views.UserOrdersListView.as_view(), name='orders-orders'),

    path('orders/order_details/<int:pk>', user_views.ItemsInOrderListView.as_view(), name='orders-order_details'),

    path('', include('restaurants.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.MEDIA_URL)
