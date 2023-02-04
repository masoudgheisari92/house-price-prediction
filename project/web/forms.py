from django import forms


class ScraperForm(forms.Form):
    SITE_CHOICES = [("divar.ir", "divar.ir")]
    CITY_CHOICES = [("tehran", "tehran"), ("isfahan", "isfahan")]
    site = forms.ChoiceField(choices=SITE_CHOICES)
    city = forms.ChoiceField(choices=CITY_CHOICES)
    num_pages = forms.IntegerField()
