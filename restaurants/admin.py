from django.contrib import admin
from . models import Food, Restaurant, Category

admin.site.register(Food)
admin.site.register(Restaurant)
admin.site.register(Category)