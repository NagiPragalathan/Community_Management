from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from base.models import CityData, Group, Connection
from base.form.forms import CityDataForm
from django.contrib.auth.decorators import login_required


def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, "index.html")

@login_required(login_url='/login/')
def dashboard(request):
    user = request.user
    group_count = Group.objects.filter(creator=user).count()
    connection_count = Connection.objects.filter(user=user, status='accepted').count()
    
    context = {
        'group_count': group_count,
        'connection_count': connection_count,
    }
    return render(request, 'dashboard.html', context)

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
