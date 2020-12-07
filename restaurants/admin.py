from django.contrib import admin
from django.utils.html import format_html

from . models import Food, FoodImage, Restaurant, Category


class FoodImageAdmin(admin.ModelAdmin):
    fields = ('food', 'image', 'thumbnail', 'image_tag')
    readonly_fields = ('thumbnail', 'image_tag')


admin.site.register(FoodImage, FoodImageAdmin)


class FoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'restaurant', 'price')
    search_fields = ('name',)
    autocomplete_fields = ('category',)
    prepopulated_fields = {"slug": ("name", )}


admin.site.register(Food, FoodAdmin)


class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'slug')
    search_fields = ('name', 'address')
    prepopulated_fields = {"slug": ("name", )}


admin.site.register(Restaurant, RestaurantAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Category, CategoryAdmin)