from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import UserDeliveryInformation, User

# Register your models here.


class UserDeliveryInformationAdmin(admin.ModelAdmin):
    fields = (
        'user',
        'image_tag',
        'read_qr_code',
        'street',
        'house_number',
        'flat_number',
        'city',
        'city_district'
    )
    readonly_fields = (
        'city',
        'image_tag',
        'read_qr_code',
        'street',
        'house_number',
        'flat_number',
        'city_district'
    )

    list_display = ('user', 'street', 'house_number', 'flat_number', 'city')


admin.site.register(UserDeliveryInformation, UserDeliveryInformationAdmin)


@admin.register(User)  # rejestracja modelu użytkownika
class UserAdmin(DjangoUserAdmin):
    '''
    Modyfikacja panelu administracyjnego, obsługującego użytkowników
    '''
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Uprawnienia",
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
            "Dodatkowe informacje o koncie",
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

