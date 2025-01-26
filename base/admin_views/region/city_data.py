from django.shortcuts import render, get_object_or_404, redirect
from base.models import CityData, CountryData, StateData

# List View
def city_list(request):
    cities = CityData.objects.all()
    return render(request, 'custom_admin/region/city_data/city_list.html', {'cities': cities})

# Create View
def city_create(request):
    if request.method == 'POST':
        city_name = request.POST['city_name']
        country_id = request.POST['country']
        state_id = request.POST['state']

        country = get_object_or_404(CountryData, id=country_id)
        state = get_object_or_404(StateData, id=state_id)

        CityData.objects.create(city_name=city_name, country=country, state=state)
        return redirect('city_list')
    countries = CountryData.objects.all()
    states = StateData.objects.all()
    return render(request, 'custom_admin/region/city_data/city_form.html', {'countries': countries, 'states': states})

# Edit View
def city_edit(request, city_id):
    city = get_object_or_404(CityData, id=city_id)
    if request.method == 'POST':
        city.city_name = request.POST['city_name']
        country_id = request.POST['country']
        state_id = request.POST['state']

        city.country = get_object_or_404(CountryData, id=country_id)
        city.state = get_object_or_404(StateData, id=state_id)
        city.save()
        return redirect('city_list')
    countries = CountryData.objects.all()
    states = StateData.objects.all()
    return render(request, 'custom_admin/region/city_data/city_form.html', {'city': city, 'countries': countries, 'states': states})

# Delete View
def city_delete(request, city_id):
    city = get_object_or_404(CityData, id=city_id)
    city.delete()
    return redirect('city_list')
