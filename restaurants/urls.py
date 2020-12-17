from django.urls import path
from .views import RestaurantListView, FoodRestaurantListView, FoodDetailView, IndexView, AboutView

urlpatterns = [
    path('', IndexView.as_view(), name='restaurants-index'),
    path('about/', AboutView.as_view(), name='restaurants-about'),
    path('restaurants/', RestaurantListView.as_view(), name='restaurants-list'),
    path('restaurants/<slug>', FoodRestaurantListView.as_view(), name='restaurants-foods'),
    path('<slug:restaurant_slug>/<slug:food_slug>', FoodDetailView.as_view(), name='food-detail'),
]