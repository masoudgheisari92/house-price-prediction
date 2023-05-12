from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

from . import forms
from .classifier import predict_price


def predict(request):
    city = request.GET.get("city")
    if city:
        if request.method == "POST":
            form = forms.HouseForm(request.POST, city=city)
            if form.is_valid():
                region = form.cleaned_data["region"]
                year_of_construction = form.cleaned_data["year_of_construction"]
                area = form.cleaned_data["area"]
                room = form.cleaned_data["room"]
                price = predict_price(region, year_of_construction, area, room)
                return HttpResponse(f"The predicted price is {price:,} tomans")
        else:
            form = forms.HouseForm(city=city)

        return render(request, "house.html", {"form": form})
    else:
        if request.method == "POST":
            form = forms.CityForm(request.POST)
            if form.is_valid():
                city = form.cleaned_data["city"]
                return HttpResponseRedirect(f"?city={city}")
        else:
            form = forms.CityForm()

        return render(request, "city.html", {"form": form})
