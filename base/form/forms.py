from django import forms
from base.models import CityData

class CityDataForm(forms.ModelForm):
    class Meta:
        model = CityData
        fields = ['city_name']
