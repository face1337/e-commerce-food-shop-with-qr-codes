from django.test import TestCase, RequestFactory, Client

from restaurants.views import IndexView, FoodRestaurantListView


class TestHomePage(TestCase):
    def test_restaurant_set_in_context(self):
        request = RequestFactory().get('/')
        view = IndexView()
        view.setup(request)

        context = view.get_context_data()
        self.assertIn('restaurant', context)
