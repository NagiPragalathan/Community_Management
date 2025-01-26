from django.shortcuts import render, get_object_or_404, redirect
from base.models import RegionPosition
from django.http import HttpResponseRedirect

# List all RegionPositions
def list_region_positions(request):
    positions = RegionPosition.objects.all()
    return render(request, 'custom_admin/region_position/list.html', {'positions': positions})

# Create a new RegionPosition
def create_region_position(request):
    if request.method == 'POST':
        name = request.POST.get('RegionpositionName')
        is_region = request.POST.get('isRegion') == 'on'
        RegionPosition.objects.create(RegionpositionName=name, isRegion=is_region)
        return redirect('list_region_positions')
    return render(request, 'custom_admin/region_position/create.html')

# Edit an existing RegionPosition
def edit_region_position(request, id):
    position = get_object_or_404(RegionPosition, id=id)
    if request.method == 'POST':
        position.RegionpositionName = request.POST.get('RegionpositionName')
        position.isRegion = request.POST.get('isRegion') == 'on'
        position.save()
        return redirect('list_region_positions')
    return render(request, 'custom_admin/region_position/edit.html', {'position': position})

# Delete a RegionPosition
def delete_region_position(request, id):
    position = get_object_or_404(RegionPosition, id=id)
    if request.method == 'POST':
        position.delete()
        return redirect('list_region_positions')
    return render(request, 'custom_admin/region_position/delete.html', {'position': position})
