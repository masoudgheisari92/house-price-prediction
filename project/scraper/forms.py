from django import forms


class ScraperForm(forms.Form):
    CITY_CHOICES = [("tehran", "tehran"), ("isfahan", "isfahan")]
    city = forms.ChoiceField(choices=CITY_CHOICES)
    num_pages_to_scrape = forms.IntegerField(label="Number of pages to scrape")
