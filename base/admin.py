from django.contrib import admin
from .models import CountryData, CityData, Region

admin.site.register(CountryData)
admin.site.register(CityData)
admin.site.register(Region)
