from django.contrib import admin
from .models import Cart, CartLine, Order, OrderLine


class CartLineInline(admin.TabularInline):
    model = CartLine
    extra = 0
    readonly_fields = ("food", "total_price", )


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status", "count")
    list_editable = ("status",)
    list_filter = ("status",)
    inlines = (CartLineInline,)


class OrderLineInline(admin.TabularInline):
    model = OrderLine
    extra = 0
    readonly_fields = ("product", "price")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status")
    list_editable = ("status",)
    list_filter = ("status", "date_placed")
    inlines = (OrderLineInline,)
    fieldsets = (
        (None, {"fields": ("user", "status")}),
        (
            "Informacje do dostawy",
            {
                "fields": (
                            "city_district",
                            "city",
                            "street",
                            "house_number",
                            "flat_number",
                            "image_tag",
                            "read_qr_code",
                            )
            },
        ),
        ("Całkowita wartośc zamówienia", {"fields": ("total_price",)}),
    )
    readonly_fields = ('user', 'city_district', 'city', 'street', 'house_number',
                       'flat_number', 'image_tag', 'read_qr_code', 'total_price')
