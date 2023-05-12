from django.contrib import admin

from .models import City, Region, House


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )
    readonly_fields = ("created_at", "updated_at")


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "city",
        "name",
    )
    readonly_fields = ("created_at", "updated_at")


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "region",
        "title",
    )
    list_filter = ("region__city",)
    readonly_fields = ("created_at", "updated_at")
