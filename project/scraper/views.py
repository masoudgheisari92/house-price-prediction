from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

from . import forms
from .scrape import Scraper


def done(request):
    return HttpResponse("done")


def scrape(request):
    if request.method == "POST":
        form = forms.ScraperForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data["city"]
            num_pages_to_scrape = form.cleaned_data["num_pages_to_scrape"]
            scraper = Scraper(city, num_pages_to_scrape)
            scraper.start()

            return HttpResponseRedirect("done/")
    else:
        form = forms.ScraperForm()

    return render(request, "scrape.html", {"form": form})
