from django.contrib import admin

from .models import City, House


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )
    readonly_fields = ("created_at", "updated_at")


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "city",
        "title",
    )
    list_filter = ("city",)
    readonly_fields = ("created_at", "updated_at")
