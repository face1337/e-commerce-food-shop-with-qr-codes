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
from users.forms import ValidateEmailForgotPassword

from users import views as user_views
from orders import views as order_views


urlpatterns = [
    path('admin/', admin.site.urls),

    path('rejestracja/', user_views.RegisterView.as_view(), name='users-register'),
    path('login/', user_views.MyLoginView.as_view(template_name='users/login.html'), name='users-login'),
    path('wyloguj/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='users-logout'),
    path('zresetuj-haslo/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html',
                                                                 form_class=ValidateEmailForgotPassword),
         name='password_reset'),
    path('zresetuj-haslo-potwierdz/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(
         template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('zresetuj-haslo/gotowe', auth_views.PasswordResetDoneView.as_view(
         template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('zresetuj-haslo/zakonczone', auth_views.PasswordResetCompleteView.as_view(
         template_name='users/password_reset_complete.html'), name='password_reset_complete'),

    path('adres/',user_views.ListOfAddressesView.as_view(), name='users-address_list'),
    path('adres/dodaj', user_views.CreateNewAddressView.as_view(), name='users-address_create'),
    path('adres/<int:pk>/zaktualizuj', user_views.UpdateAddressView.as_view(), name='users-address_update'),
    path('address/<int:pk>/delete', user_views.DeleteAddressView.as_view(), name='users-address_confirm_delete'),

    path('dodaj-do-koszyka/', order_views.add_to_cart, name='orders-add_to_cart'),
    path('koszyk/', order_views.manage_cart, name='orders-cart'),
    path('zamowienia/wybor-adresu-dostawy', user_views.SelectAddressView.as_view(), name='users-address_select'),
    path('zamowienia/<str:email>', user_views.UserOrdersListView.as_view(), name='orders-orders'),
    path('zamowienia/szczegoly-zamowienia/<int:pk>', user_views.ItemsInOrderListView.as_view(), name='orders-order_details'),

    path('statystyki', order_views.StatisticsView.as_view(), name='orders-statistics'),
    path('', include('restaurants.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.MEDIA_URL)
