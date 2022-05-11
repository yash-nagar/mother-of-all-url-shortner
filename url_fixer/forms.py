from django import forms
from .models import UrlData


class ShortenerForm(forms.Form):
    custom_url = forms.SlugField(max_length=10, required=False)
    long_url = forms.URLField(widget=forms.URLInput(
        attrs={"class": "form-control form-control-lg", "placeholder": "Your URL to shorten"}))

    def clean(self):
        if self.errors:
            return False
        form_data = self.cleaned_data
        custom_url = form_data['custom_url']
        if UrlData.objects.filter(short_url=custom_url).exists():
            raise forms.ValidationError({'custom_url': "This Url is already take. Please choose another"})
        return form_data
