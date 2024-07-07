from django import forms
from django.contrib.auth.models import User
from base.models import TYFCB
from django_select2.forms import ModelSelect2Widget

class TYFCBForm(forms.ModelForm):
    thank_you_to = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=ModelSelect2Widget(
            model=User,
            search_fields=['username__icontains', 'first_name__icontains', 'last_name__icontains'],
            attrs={'data-placeholder': 'Search for a user...'}
        ),
        required=False,
    )

    class Meta:
        model = TYFCB
        fields = ['chapter_name', 'region_name', 'referral_amount', 'business_type', 'referral_type', 'comments', 'thank_you_to']
        widgets = {
            'business_type': forms.RadioSelect,
            'referral_type': forms.RadioSelect,
        }

class ReferralFilterForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))



# class OneToOneSlipForm(forms.ModelForm):
#     class Meta:
#         model = OneToOneSlip
#         fields = ['region_name', 'chapter_name', 'invited_by', 'location', 'conversation', 'date']
#         widgets = {
#             'region_name': forms.Select(attrs={'required': 'required'}),
#             'chapter_name': forms.Select(attrs={'required': 'required'}),
#             'invited_by': forms.Select(attrs={'required': 'required'}),
#             'location': forms.TextInput(attrs={'required': 'required'}),
#             'conversation': forms.Textarea(attrs={'required': 'required'}),
#             'date': forms.DateInput(attrs={'type': 'date', 'required': 'required'}),
#         }




# class ChapterEdUnitForm(forms.ModelForm):
#     class Meta:
#         model = ChapterEdUnit
#         fields = ['course_title', 'credits', 'total_credit_last_week']

