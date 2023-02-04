from django.shortcuts import render

from . import forms


def base(request):
    return render(request, "base.html")


def scraper(request):
    form = forms.ScraperForm()
    return render(request, "scraper.html", {"form": form})
