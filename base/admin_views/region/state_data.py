from django.shortcuts import render, redirect, get_object_or_404
from base.models import CountryData, StateData

def state_list(request):
    states = StateData.objects.select_related('country').all()
    return render(request, 'custom_admin/region/state_data/state_list.html', {'states': states})

def state_create(request):
    countries = CountryData.objects.all()  # Provide countries to associate a state
    if request.method == "POST":
        state_name = request.POST.get('state_name')
        country_id = request.POST.get('country_id')
        country = get_object_or_404(CountryData, id=country_id)
        if state_name:
            StateData.objects.create(state_name=state_name, country=country)
        return redirect('state_list')
    return render(request, 'custom_admin/region/state_data/state_form.html', {'countries': countries, 'operation': 'Create'})

def state_edit(request, state_id):
    state = get_object_or_404(StateData, id=state_id)
    countries = CountryData.objects.all()  # Provide countries for potential reassignment   
    if request.method == "POST":
        state_name = request.POST.get('state_name')
        country_id = request.POST.get('country_id')
        country = get_object_or_404(CountryData, id=country_id)
        if state_name:
            state.state_name = state_name
            state.country = country
            state.save()
        return redirect('state_list')
    return render(request, 'custom_admin/region/state_data/state_form.html', {'state': state, 'countries': countries, 'operation': 'Edit'})

def state_delete(request, state_id):
    state = get_object_or_404(StateData, id=state_id)
    if request.method == "POST":
        state.delete()
        return redirect('state_list')
    return render(request, 'custom_admin/region/state_data/state_confirm_delete.html', {'state': state})
