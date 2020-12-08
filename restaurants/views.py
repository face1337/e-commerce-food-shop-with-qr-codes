from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView
from .models import Restaurant, Food


class IndexView(TemplateView):
    template_name = 'restaurants/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['restaurant'] = Restaurant.objects.first()
        return context


class FoodRestaurantListView(ListView):
    model = Food
    template_name = 'restaurants/restaurant_foods.html'
    context_object_name = 'foods'


class FoodDetailView(DetailView):
    model = Food
    template_name = 'restaurants/food_detail.html'
    context_object_name = 'food_detail'
