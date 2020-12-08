from django.test import TestCase
from django.urls import reverse, resolve
from ..views import index, FoodRestaurantListView, FoodDetailView


class TestUrls(TestCase):

    def test_index_url(self):
        pass
