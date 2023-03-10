from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

from . import forms
from .scrape import Scraper


def base(request):
    return render(request, "base.html")


def done(request):
    return HttpResponse("done")


def scraper(request):
    if request.method == "POST":
        form = forms.ScraperForm(request.POST)
        if form.is_valid():
            website = form.cleaned_data["website"]
            city = form.cleaned_data["city"]
            num_pages_to_scrape = form.cleaned_data["num_pages_to_scrape"]
            scraper = Scraper(website, city)
            scraper.start()

            return HttpResponseRedirect("/done/")
    else:
        form = forms.ScraperForm()

    return render(request, "scraper.html", {"form": form})
