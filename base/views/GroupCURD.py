from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from base.models import Group, Room, Message
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q


@login_required
def list_groups(request):
    user = request.user
    groups = Group.objects.filter(
        Q(group_type="Open") | Q(creator=user) | Q(members=user)
    ).distinct()
    return render(request, 'Group/listGroup.html', {'groups': groups})

@login_required
def my_list_groups(request):
    groups = Group.objects.filter(members=request.user)
    return render(request, 'Group/my_group.html', {'groups': groups})

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
            return redirect('list_groups')
        else:
            user_groups_count = Group.objects.filter(creator=request.user).count()
            if not pk and user_groups_count >= 5:
                messages.error(request, "You have reached the maximum number of groups (5).")
                return redirect('group_crud_new')

            name = request.POST.get('name')
            group_type = request.POST.get('group_type')
            access_type = request.POST.get('access_type')
            language = request.POST.get('language')
            description = request.POST.get('description')
            logo = request.FILES.get('logo')

            if not group:
                group = Group(creator=request.user)

            group.name = name
            group.group_type = group_type
            group.access_type = access_type
            group.language = language
            group.description = description

            if logo:
                group.logo = logo

            group.save()

            if not pk:  # Only increase the group count if a new group is created
                group.group_counts += 1
                group.save()

            return redirect('list_groups')  # Redirect to the list of groups after saving
    else:
        group_data = {
            'name': group.name if group else '',
            'group_type': group.group_type if group else '',
            'access_type': group.access_type if group else '',
            'language': group.language if group else '',
            'description': group.description if group else '',
        }

    groups = Group.objects.all()
    return render(request, 'Group/group_crud.html', {'group_data': group_data, 'groups': groups, 'group': group})

@login_required
def join_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.user not in group.members.all():
        group.members.add(request.user)
        redirect("chat/"+group.name)
    else:
        print("User already exist..!")
    return redirect('room', room_name=group.name)

@login_required
def room(request, room_name):
    room, created = Room.objects.get_or_create(name=room_name)
    group = get_object_or_404(Group, name=room_name)
    if request.user not in group.members.all():
        return redirect('list_groups')
    messages = Message.objects.filter(room=room).order_by('timestamp')
    return render(request, 'Group/room.html', {'room_name': room_name, 'room': room, 'messages': messages, 'group': group})

@login_required
@require_POST
def send_message(request, room_name):
    room = get_object_or_404(Room, name=room_name)
    group = get_object_or_404(Group, name=room_name)
    if request.user not in group.members.all():
        return JsonResponse({'error': 'You are not a member of this group.'}, status=403)
    message = Message.objects.create(
        room=room,
        user=request.user,
        content=request.POST['message']
    )
    return JsonResponse({'message': message.content, 'user': message.user.username, 'timestamp': message.timestamp})

@login_required
def get_messages(request, room_name):
    room = get_object_or_404(Room, name=room_name)
    group = get_object_or_404(Group, name=room_name)
    if request.user not in group.members.all():
        return JsonResponse({'error': 'You are not a member of this group.'}, status=403)
    messages = Message.objects.filter(room=room).order_by('timestamp')
    messages_data = [{'user': message.user.username, 'message': message.content, 'timestamp': message.timestamp} for message in messages]
    return JsonResponse({'messages': messages_data})

@login_required
def joined_groups(request):
    user = request.user
    groups = Group.objects.filter(members=user).distinct()
    return render(request, 'Group/joined_groups.html', {'groups': groups})