from django.urls import reverse, resolve
from django.test import TestCase
from restaurants.views import IndexView, AboutView, FoodRestaurantListView, FoodDetailView


class TestUrls(TestCase):
    """
    Testy dla utworzonych urlsow w aplikacji 'restaurants', jesli testy nie zwracają błędu
    oznacza to, że każdy link (url) jest poprawny
    """
    def test_index_url(self):
        url = reverse('restaurants-index')
        self.assertEquals(resolve(url).func.view_class, IndexView)

    def test_about_url(self):
        url = reverse('restaurants-about')
        self.assertEquals(resolve(url).func.view_class, AboutView)

    def test_food_list_url(self):
        url = reverse('restaurant-foods', args=['test-slug'])
        self.assertEquals(resolve(url).func.view_class, FoodRestaurantListView)

    def test_food_detail_url(self):
        url = reverse('food-detail', args=['test-slug'])
        self.assertEquals(resolve(url).func.view_class, FoodDetailView)


