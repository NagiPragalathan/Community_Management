from django import forms
from base.models import CityData, ChapterPosition
from django.contrib.auth.models import User

class CityDataForm(forms.ModelForm):
    class Meta:
        model = CityData
        fields = ['city_name']
