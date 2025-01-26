from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import (
    CountryData, CityData, Region, RegionPosition, RegionMemberPosition, Group,
    Chapter, ChapterMemberPosition, ChapterPosition, MainProfile, ChapterName, StateData
)
from django import forms
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

from django.contrib import messages
from django.shortcuts import redirect

from django.core.exceptions import ValidationError
from django.forms import ModelForm
    


class ChapterMemberPositionInline(admin.TabularInline):
    model = ChapterMemberPosition
    extra = 1
    autocomplete_fields = ['user', 'position']

class MainProfileInline(admin.TabularInline):
    model = Chapter.chapter_members.through
    extra = 1
    autocomplete_fields = ['mainprofile']

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        original_init = formset.__init__

        def formset_init(self, *args, **kwargs):
            original_init(self, *args, **kwargs)
            for form in self.forms:
                if obj is not None:
                    form.fields['chapter'].queryset = Chapter.objects.filter(pk=obj.pk)
                    form.fields['mainprofile'].queryset = MainProfile.objects.all()
                    form.initial['chapter'] = obj

        formset.__init__ = formset_init
        return formset

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('name', 'region', 'country', 'city', 'type', 'day', 'last_updated_date')
    search_fields = ('name', 'region__region_name', 'country__country_name', 'city__city_name')
    list_filter = ('region', 'country', 'city', 'type', 'day')
    inlines = [ChapterMemberPositionInline, MainProfileInline]
    exclude = ['member_positions', 'chapter_members']
    autocomplete_fields = ['region', 'country', 'city', 'chapter_members']
    filter_horizontal = ['chapter_members']

    def save_model(self, request, obj, form, change):
        # if MainProfile.objects.count() < 1:
        #     storage = messages.get_messages(request)
        #     for _ in storage:
        #         pass  # Clear existing messages
        #         print(_)
        #     messages.error(request, "You need at least 5 MainProfile instances to create a Chapter.")
        # else:
        super().save_model(request, obj, form, change)        
        
@admin.register(CountryData)
class CountryDataAdmin(admin.ModelAdmin):
    list_display = ('country_name', 'last_updated_date')
    search_fields = ('country_name',)
    list_filter = ('last_updated_date',)

@admin.register(CityData)
class CityDataAdmin(admin.ModelAdmin):
    list_display = ('city_name', 'country', 'last_updated_date')
    search_fields = ('city_name', 'country__country_name')
    list_filter = ('country', 'last_updated_date')
    autocomplete_fields = ['country']

@admin.register(StateData)
class StateDataAdmin(admin.ModelAdmin):
    list_display = ('state_name', 'country', 'last_updated_date')
    search_fields = ('state_name', 'country__country_name')
    list_filter = ('country', 'last_updated_date')
    autocomplete_fields = ['country']

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('region_name', 'country', 'city', 'last_updated_date')
    search_fields = ('region_name', 'country__country_name', 'city__city_name')
    list_filter = ('country', 'city', 'last_updated_date')
    autocomplete_fields = ['country', 'city']

@admin.register(RegionPosition)
class RegionPositionAdmin(admin.ModelAdmin):
    # list_display = ('RegionpositionName', 'lastupdateddate', 'isRegion')
    list_display = ('RegionpositionName', 'isRegion')
    search_fields = ('RegionpositionName',)
    list_filter = ('isRegion',)

@admin.register(RegionMemberPosition)
class MemberPositionAdmin(admin.ModelAdmin):
    list_display = ('user', 'position')
    search_fields = ('user__username', 'position__RegionpositionName')
    list_filter = ('position',)
    autocomplete_fields = ['user', 'position']

@admin.register(ChapterMemberPosition)
class ChapterMemberPositionAdmin(admin.ModelAdmin):
    list_display = ('user', 'position', 'chapter')
    search_fields = ('user__username', 'position__Chapterposition', 'chapter__name__chapter_name')
    list_filter = ('chapter', 'position', 'user')
    autocomplete_fields = ['user', 'position', 'chapter']

@admin.register(ChapterPosition)
class ChapterPositionAdmin(admin.ModelAdmin):
    list_display = ('Chapterposition', 'is_chapter', 'lastupdateddate')
    search_fields = ('Chapterposition',)
    list_filter = ('is_chapter', 'lastupdateddate')

@admin.register(ChapterName)
class ChapterNameAdmin(admin.ModelAdmin):
    list_display = ('chapter_name', 'last_updated_date')
    search_fields = ('chapter_name',)
    list_filter = ('last_updated_date',)

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator', 'group_type', 'access_type', 'lastupdateddate')
    search_fields = ('name', 'creator__username', 'group_type', 'access_type')
    list_filter = ('group_type', 'access_type', 'lastupdateddate')

    fieldsets = (
        (None, {
            'fields': ('name', 'creator', 'group_type', 'access_type', 'language', 'logo', 'invite_connections', 'description')
        }),
    )
    

    
@admin.action(description='Reactivate selected memberships')
def reactivate_memberships(modeladmin, request, queryset):
    for profile in queryset:
        if profile.membership_status == 'Not Active':
            profile.membership_status = 'Active'
            profile.renewal_due_date = timezone.now().date() + timedelta(days=365)
            profile.active_until = None
            profile.save()

class MainProfileForm(ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')

        if not first_name or not last_name:
            raise ValidationError("Both 'first name' and 'last name' are required.")
        
        return cleaned_data

@admin.register(MainProfile)
class MainProfileAdmin(admin.ModelAdmin):
    form = MainProfileForm  # Use the custom form
    list_display = ('uuid', 'user', 'first_name', 'last_name', 'membership_status', 'renewal_due_date')
    search_fields = ('first_name', 'last_name', 'user__username')
    list_filter = ('membership_status', 'gender', 'industry')
    autocomplete_fields = ['user', 'Chapter']
    readonly_fields = ['uuid']

    fieldsets = (
        (None, {
            'fields': ('uuid', 'user', 'title', 'first_name', 'last_name', 'suffix', 'display_name', 'gender')
        }),
        ('Company Info', {
            'fields': ('company_name', 'product_service_description', 'gst_registered_state', 'gst_identification_number_or_pan', 'industry', 'classification')
        }),
        ('Membership Info', {
            'fields': ('requested_speciality', 'membership_status', 'renewal_due_date', 'Chapter')
        }),
        ('Additional Info', {
            'fields': ('my_business', 'keywords')
        }),
    )

    def save_model(self, request, obj, form, change):
        if form.is_valid():
            super().save_model(request, obj, form, change)
        else:
            # Display error message if form is invalid
            messages.error(request, "The form contains errors. Please correct them before saving.")
    def save_model(self, request, obj, form, change):
        if not obj.first_name or not obj.last_name:
            # Display an error message instead of raising an exception
            messages.error(request, "First name and last name are required. The changes were not saved.")
        else:
            super().save_model(request, obj, form, change)
