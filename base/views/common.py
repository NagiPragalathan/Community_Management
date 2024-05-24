from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from base.models import CityData
from base.form.forms import CityDataForm


def home(request):
    return render(request, "home.html")

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Country >>>>>>>>>>>>>>>>>>>>>>>>


# View to add a new city
def add_city(request):
    city = CityData.objects.all()
    if request.method == 'POST':
        form = CityDataForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_city')
    else:
        form = CityDataForm()
    return render(request, 'region/city_form.html', {'form': form, 'city':city})
