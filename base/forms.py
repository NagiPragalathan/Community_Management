from django import forms
from .models import TYFCB
from .models import Referral
from .models import OneToOneSlip
from .models import ChapterEdUnit

class TYFCBForm(forms.ModelForm):
    class Meta:
        model = TYFCB
        fields = ['chapter_name', 'region_name', 'referral_amount', 'business_type', 'referral_type', 'comments']
        widgets = {
            'business_type': forms.RadioSelect,
            'referral_type': forms.RadioSelect,
        }


class ReferralForm(forms.ModelForm):
    class Meta:
        model = Referral
        fields = [
            'chapter_name', 
            'region_name', 
            'referral', 
            'referral_type', 
            'referral_status', 
            'address', 
            'telephone', 
            'email', 
            'comments'
        ]
        widgets = {
            'referral_type': forms.RadioSelect,
            'referral_status': forms.CheckboxSelectMultiple,
            'address': forms.Textarea(attrs={'rows': 2}),
            'comments': forms.Textarea(attrs={'rows': 2}),
        }


class OneToOneSlipForm(forms.ModelForm):
    class Meta:
        model = OneToOneSlip
        fields = ['region_name', 'chapter_name', 'invited_by', 'location', 'conversation', 'date']
        widgets = {
            'region_name': forms.Select(attrs={'required': 'required'}),
            'chapter_name': forms.Select(attrs={'required': 'required'}),
            'invited_by': forms.Select(attrs={'required': 'required'}),
            'location': forms.TextInput(attrs={'required': 'required'}),
            'conversation': forms.Textarea(attrs={'required': 'required'}),
            'date': forms.DateInput(attrs={'type': 'date', 'required': 'required'}),
        }




class ChapterEdUnitForm(forms.ModelForm):
    class Meta:
        model = ChapterEdUnit
        fields = ['course_title', 'credits', 'total_credit_last_week']

class QtyEarnedForm(forms.ModelForm):
    class Meta:
        model = ChapterEdUnit
        fields = ['qty_earned']
        widgets = {
            'qty_earned': forms.NumberInput(attrs={'required': 'true'}),
        }
