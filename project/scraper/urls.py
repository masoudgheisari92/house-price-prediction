from django.urls import path

from . import views


urlpatterns = [
    path("", views.base),
    path("scrape/", views.scrape),
    path("done/", views.done),
]
