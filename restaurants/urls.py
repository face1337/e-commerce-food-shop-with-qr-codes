from django.urls import path
from . import views
from .views import FoodRestaurantListView

urlpatterns = [
    path('', views.index, name='restaurants-index'),
    path('restaurant/<slug>', FoodRestaurantListView.as_view(), name='restaurant-foods'),
]