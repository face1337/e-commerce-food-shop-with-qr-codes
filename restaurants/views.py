from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import DetailView, ListView
from .models import Restaurant, Food, Category


def index(request):
    context = {
        'restaurants': Restaurant.objects.all(),
    }
    return render(request, 'restaurants/index.html', context)


class FoodRestaurantListView(ListView):
    model = Food
    template_name = 'restaurants/restaurant_foods.html'
    context_object_name = 'foods'

    def get_queryset(self):
        restaurant = get_object_or_404(Restaurant, slug=self.kwargs.get('slug'))
        return Food.objects.filter(restaurant=restaurant)


class FoodDetailView(DetailView):
    model = Food
    template_name = 'restaurants/food_detail.html'
    context_object_name = 'food_detail'



