from django.urls import path
from . import views
from .views import FoodRestaurantListView, FoodDetailView, IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='restaurants-index'),
    path('restaurant/<slug>', FoodRestaurantListView.as_view(), name='restaurant-foods'),
    path('food/<slug>', FoodDetailView.as_view(), name='food-detail'),
]