from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import DetailView
from .models import Restaurant


def index(request):
    context = {
        'restaurants':Restaurant.objects.all()
    }
    return render(request, 'restaurants/index.html', context)


class RestaurantDetailView(DetailView):
    model = Restaurant
