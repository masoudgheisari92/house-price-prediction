from django import forms

from core.models import City, Region


class CityForm(forms.Form):
    city = forms.ModelChoiceField(queryset=City.objects.all())


class HouseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        city_name = kwargs.pop("city")
        self.city = City.objects.get(name=city_name)
        super().__init__(*args, **kwargs)

        self.fields["region"] = forms.ModelChoiceField(
            queryset=Region.objects.filter(city=self.city)
        )

    year_of_construction = forms.IntegerField(
        initial=1402, max_value=1402, min_value=1370
    )
    area = forms.IntegerField(initial=100, min_value=0)
    room = forms.IntegerField(initial=0, min_value=0)
