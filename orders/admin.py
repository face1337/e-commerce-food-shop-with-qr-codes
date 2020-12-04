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


class OrderLineInline(admin.StackedInline):
    model = OrderLine
    extra = 0
    readonly_fields = ("product",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status")
    list_editable = ("status",)
    list_filter = ("status", "date_placed")
    inlines = (OrderLineInline,)
    fieldsets = (
        (None, {"fields": ("user", "status")}),
        (
            "Informacje do wysyłki",
            {
                "fields": (
                            "shipping_address1",
                            "shipping_address2",
                            "house_number",
                            "flat_number",
                            "image_tag",
                            "read_qr_code",
                            )
                    },
                ),
    )
    readonly_fields = ('user', 'shipping_address1', 'shipping_address2', 'house_number',
                       'flat_number','image_tag', 'read_qr_code',)