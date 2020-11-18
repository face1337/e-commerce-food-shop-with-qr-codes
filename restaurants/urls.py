from django.urls import path
from . import views
from .views import RestaurantDetailView

urlpatterns = [
    path('', views.index, name='restaurants-index'),
    path('restaurant/<slug>', RestaurantDetailView.as_view(), name='restaurant-detail'),
]