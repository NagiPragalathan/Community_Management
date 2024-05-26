from django.contrib.admin import AdminSite
from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import (
    CountryData, CityData, Region, RegionPosition, RegionMemberPosition,
    Chapter, ChapterMemberPosition, ChapterPosition, MainProfile, ChapterName
)
from django import forms
from django.contrib.auth.models import User

class Admin(AdminSite):
    site_header = 'Victory Connect Admin'
    site_title = 'Admin Portal'
    index_title = 'Welcome to Victory Connect Admin Portal'

admin_site = Admin(name='admin')
admin_site.register(User)

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

class ChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        exclude = ['member_positions']

    def clean_chapter_members(self):
        chapter_members = self.cleaned_data.get('chapter_members')
        if not chapter_members.exists():
            raise ValidationError("You need at least one Chapter member to create a Chapter.")
        return chapter_members

admin_site.register(MainProfile)
class MainProfileAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'user', 'first_name', 'last_name', 'membership_status', 'RenewalDueDate')
    search_fields = ('first_name', 'last_name', 'user__username')
    list_filter = ('membership_status', 'gender', 'industry')
    autocomplete_fields = ['user', 'Chapter']
    readonly_fields = ['uuid']
    # filter_horizontal = ['']

    fieldsets = (
        (None, {
            'fields': ('uuid', 'user', 'title', 'first_name', 'last_name', 'suffix', 'display_name', 'gender')
        }),
        ('Company Info', {
            'fields': ('company_name', 'product_service_description', 'gst_registered_state', 'gst_identification_number_or_pan', 'industry', 'classification')
        }),
        ('Membership Info', {
            'fields': ('requested_speciality', 'membership_status', 'RenewalDueDate', 'Chapter')
        }),
        ('Additional Info', {
            'fields': ('my_business', 'keywords')
        }),
    )

    def save_model(self, request, obj, form, change):
        if not obj.first_name or not obj.last_name:
            raise ValidationError("First name and last name are required.")
        super().save_model(request, obj, form, change)

admin_site.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('name', 'region', 'country', 'city', 'type', 'day', 'last_updated_date')
    search_fields = ('name', 'region__region_name', 'country__country_name', 'city__city_name')
    list_filter = ('region', 'country', 'city', 'type', 'day')
    inlines = [ChapterMemberPositionInline, MainProfileInline]
    exclude = ['member_positions', 'chapter_members']
    autocomplete_fields = ['region', 'country', 'city', 'chapter_members']
    filter_horizontal = ['chapter_members']
    

    def save_model(self, request, obj, form, change):
        if MainProfile.objects.count() < 5:
            raise ValidationError("You need at least 5 MainProfile instances to create a Chapter.")
        super().save_model(request, obj, form, change)
admin_site.register(CountryData)
class CountryDataAdmin(admin.ModelAdmin):
    list_display = ('country_name', 'last_updated_date')
    search_fields = ('country_name',)
    list_filter = ('last_updated_date',)

admin_site.register(CityData)
class CityDataAdmin(admin.ModelAdmin):
    list_display = ('city_name', 'country', 'last_updated_date')
    search_fields = ('city_name', 'country__country_name')
    list_filter = ('country', 'last_updated_date')
    autocomplete_fields = ['country']

admin_site.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('region_name', 'country', 'city', 'last_updated_date')
    search_fields = ('region_name', 'country__country_name', 'city__city_name')
    list_filter = ('country', 'city', 'last_updated_date')
    autocomplete_fields = ['country', 'city']

admin_site.register(RegionPosition)
class RegionPositionAdmin(admin.ModelAdmin):
    list_display = ('RegionpositionName', 'lastupdateddate', 'isRegion')
    search_fields = ('RegionpositionName',)
    list_filter = ('isRegion', 'lastupdateddate')

admin_site.register(RegionMemberPosition)
class MemberPositionAdmin(admin.ModelAdmin):
    list_display = ('user', 'position')
    search_fields = ('user__username', 'position__RegionpositionName')
    list_filter = ('position',)
    autocomplete_fields = ['user', 'position']

admin_site.register(ChapterMemberPosition)
class ChapterMemberPositionAdmin(admin.ModelAdmin):
    list_display = ('user', 'position', 'chapter')
    search_fields = ('user__username', 'position__Chapterposition', 'chapter__name__chapter_name')
    list_filter = ('chapter', 'position', 'user')
    autocomplete_fields = ['user', 'position', 'chapter']

admin_site.register(ChapterPosition)
class ChapterPositionAdmin(admin.ModelAdmin):
    list_display = ('Chapterposition', 'is_chapter', 'lastupdateddate')
    search_fields = ('Chapterposition',)
    list_filter = ('is_chapter', 'lastupdateddate')

admin_site.register(ChapterName)
class ChapterNameAdmin(admin.ModelAdmin):
    list_display = ('chapter_name', 'last_updated_date')
    search_fields = ('chapter_name',)
    list_filter = ('last_updated_date',)
