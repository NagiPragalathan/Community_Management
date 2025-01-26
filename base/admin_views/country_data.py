from django.shortcuts import render, redirect, get_object_or_404
from base.models import CountryData

def country_list(request):
    countries = CountryData.objects.all()
    return render(request, 'custom_admin/country_data/country_list.html', {'countries': countries})

def country_create(request):
    if request.method == "POST":
        country_name = request.POST.get('country_name')
        if country_name:
            CountryData.objects.create(country_name=country_name)
        return redirect('country_list')
    return render(request, 'custom_admin/country_data/country_form.html', {'operation': 'Create'})

def country_edit(request, pk):
    country = get_object_or_404(CountryData, pk=pk)
    if request.method == "POST":
        country_name = request.POST.get('country_name')
        if country_name:
            country.country_name = country_name
            country.save()
        return redirect('country_list')
    return render(request, 'custom_admin/country_data/country_form.html', {'country': country, 'operation': 'Edit'})

def country_delete(request, pk):
    country = get_object_or_404(CountryData, pk=pk)
    if request.method == "POST":
        country.delete()
        return redirect('country_list')
    return render(request, 'custom_admin/country_data/country_confirm_delete.html', {'country': country})
