from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView, TemplateView
from .models import Restaurant, Food


class IndexView(TemplateView):
    template_name = 'restaurants/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['restaurant'] = Restaurant.objects.all()
        return context


class AboutView(TemplateView):
    template_name = 'restaurants/about.html'


class RestaurantListView(ListView):
    model = Restaurant
    template_name = 'restaurants/restaurant_list.html'
    context_object_name = 'restaurants'


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
