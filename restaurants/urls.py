from django.urls import path
from .views import RestaurantListView, FoodRestaurantListView, FoodDetailView, IndexView, AboutView

urlpatterns = [
    path('', IndexView.as_view(), name='restaurants-index'),
    path('o-stronie/', AboutView.as_view(), name='restaurants-about'),
    path('restauracje/', RestaurantListView.as_view(), name='restaurants-list'),
    path('restauracje/<slug>', FoodRestaurantListView.as_view(), name='restaurants-foods'),
    path('restauracje/<slug:restaurant_slug>/<slug:food_slug>', FoodDetailView.as_view(), name='food-detail'),
]