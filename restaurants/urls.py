from django.urls import path
from .views import RestaurantListView, FoodRestaurantListView, FoodDetailView, IndexView, AboutView

urlpatterns = [
    path('', IndexView.as_view(), name='restaurants-index'),
    path('about/', AboutView.as_view(), name='restaurants-about'),
    path('restaurants/', RestaurantListView.as_view(), name='restaurants-list'),
    path('restaurant/<slug>', FoodRestaurantListView.as_view(), name='restaurant-foods'),
    path('food/<slug>', FoodDetailView.as_view(), name='food-detail'),
]