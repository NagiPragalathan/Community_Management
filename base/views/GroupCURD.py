# myapp/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from base.models import Group
from base.form.forms import GroupForm

@login_required
def list_groups(request):
    groups = Group.objects.all()
    return render(request, 'Group/listGroup.html', {'groups': groups})

@login_required
def group_crud(request, pk=None):
    if pk:
        group = get_object_or_404(Group, pk=pk)
    else:
        group = None

    if request.method == 'POST':
        if 'delete' in request.POST:
            if group:
                group.delete()
            return redirect('group_crud')
        else:
            if not pk and Group.objects.filter(creator=request.user).count() >= settings.MAX_GROUPS_PER_USER:
                messages.error(request, "You cannot create more than {} groups.".format(settings.MAX_GROUPS_PER_USER))
                return redirect('group_crud')

            form = GroupForm(request.POST, request.FILES, instance=group)
            if form.is_valid():
                group = form.save(commit=False)
                if not pk:  # Only set the creator if the group is new
                    group.creator = request.user
                group.save()
                form.save_m2m()  # Save many-to-many relationships
                return redirect('group_crud')
    else:
        form = GroupForm(instance=group)

    groups = Group.objects.all()
    return render(request, 'Group/group_crud.html', {'form': form, 'groups': groups, 'group': group})
