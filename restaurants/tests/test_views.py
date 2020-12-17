from django.test import TestCase, RequestFactory, Client

from restaurants.models import Restaurant
from restaurants.views import IndexView, FoodRestaurantListView


class TestHomePage(TestCase):

    def test_restaurant_set_in_context_IndexView(self):
        request = RequestFactory().get('/')
        view = IndexView()
        view.setup(request)

        context = view.get_context_data()
        self.assertIn('restaurant', context)


class TestRestaurantListView(TestCase):

    def test_correct_template(self):
        response = self.client.get(f'/restaurants/')
        self.assertTemplateUsed(response, 'restaurants/restaurant_list.html')

    def test_display_all_restaurants(self):
        number_of_restaurants_ = 5
        for restaurant_slug_ in number_of_restaurants_:
            Restaurant.objects.create(

            )
