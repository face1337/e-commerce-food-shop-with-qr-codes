from django.contrib import admin
from django.utils.html import format_html

from . models import Food, FoodImage, Restaurant, Category

admin.site.register(Category)
admin.site.register(FoodImage)


class FoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'restaurant', 'price')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name", )}


admin.site.register(Food, FoodAdmin)


class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'slug')
    search_fields = ('name', 'address')
    prepopulated_fields = {"slug": ("name", )}


admin.site.register(Restaurant, RestaurantAdmin)