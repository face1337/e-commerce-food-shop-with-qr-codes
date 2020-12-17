from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView, TemplateView
from django.utils.translation import gettext_lazy as _
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

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        restaurant_slug = self.kwargs.get('restaurant_slug', None)
        food_slug = self.kwargs.get('food_slug', None)
        food_id = self.kwargs.get('food_id')
        try:
            obj = queryset.get(slug=food_slug, restaurant__slug=restaurant_slug)
        except queryset.model.DoesNotExist:
            raise Http404(_("Nie znaleziono takiego posiłku"))
        return obj
