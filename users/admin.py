from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import Address, User

# Register your models here.


class AddressAdmin(admin.ModelAdmin):
    fields = (
        'user',
        'image_tag',
        'read_qr_code',
        'address2',
        'house_number',
        'flat_number',
        'address1',
        'city_district'
    )
    readonly_fields = (
        'address1',
        'image_tag',
        'read_qr_code',
        'address2',
        'house_number',
        'flat_number',
        'city_district'
    )

    list_display = ('user', 'address2', 'house_number', 'flat_number', 'address1')


admin.site.register(Address, AddressAdmin)


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal info",
            {"fields": ("first_name", "last_name")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            "Important dates",
            {"fields": ("last_login", "date_joined")},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_staff",
    )
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)

