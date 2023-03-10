from django import forms


class ScraperForm(forms.Form):
    WEBSITE_CHOICES = [("divar", "divar")]
    CITY_CHOICES = [("tehran", "tehran"), ("isfahan", "isfahan")]
    website = forms.ChoiceField(choices=WEBSITE_CHOICES)
    city = forms.ChoiceField(choices=CITY_CHOICES)
    num_pages_to_scrape = forms.IntegerField(label="Number of pages to scrape")
