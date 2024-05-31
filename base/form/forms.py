from django import forms
from base.models import CityData, Group
from django.contrib.auth.models import User
from django_select2.forms import Select2MultipleWidget

class CityDataForm(forms.ModelForm):
    class Meta:
        model = CityData
        fields = ['city_name']


class GroupForm(forms.ModelForm):
    invite_connections = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=Select2MultipleWidget,
        required=False
    )

    class Meta:
        model = Group
        fields = ['name', 'group_type', 'access_type', 'language', 'logo', 'invite_connections', 'description']
        widgets = {
            'logo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        
        
        