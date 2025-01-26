from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from base.models import RegionMemberPosition, User, RegionPosition, Region

def region_member_position_list(request):
    positions = RegionMemberPosition.objects.all()
    return render(request, 'custom_admin/region/region_member_position/region_member_position_list.html', {'positions': positions})

def region_member_position_create(request):
    if request.method == 'POST':
        user_id = request.POST.get('user')
        position_id = request.POST.get('position')
        region_id = request.POST.get('region')

        user = User.objects.get(id=user_id)
        position = RegionPosition.objects.get(id=position_id)
        region = Region.objects.get(id=region_id)

        RegionMemberPosition.objects.create(user=user, position=position, region=region)
        return redirect('region_member_position_list')

    users = User.objects.all()
    positions = RegionPosition.objects.all()
    regions = Region.objects.all()
    return render(request, 'custom_admin/region/region_member_position/region_member_position_form.html', {
        'users': users, 'positions': positions, 'regions': regions, 'operation': 'Create'
    })


def region_member_position_edit(request, id):
    position = RegionMemberPosition.objects.get(id=id)
    if request.method == 'POST':
        user_id = request.POST.get('user')
        position_id = request.POST.get('position')
        region_id = request.POST.get('region')

        position.user = User.objects.get(id=user_id)
        position.position = RegionPosition.objects.get(id=position_id)
        position.region = Region.objects.get(id=region_id)
        position.save()
        return redirect('region_member_position_list')

    users = User.objects.all()
    positions = RegionPosition.objects.all()
    regions = Region.objects.all()
    return render(request, 'custom_admin/region/region_member_position/region_member_position_form.html', {
        'users': users, 'positions': positions, 'regions': regions,
        'operation': 'Edit', 'position': position
    })


def region_member_position_delete(request, id):
    position = RegionMemberPosition.objects.get(id=id)
    if request.method == 'POST':
        position.delete()
        return redirect('region_member_position_list')
    return render(request, 'custom_admin/region/region_member_position/region_member_position_confirm_delete.html', {'position': position})
