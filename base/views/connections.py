from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from base.models import Connection, MainProfile
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import messages

@login_required
def connection_list(request, username=None):
    if username:
        user = User.objects.get(username=username)
    else:
        user = request.user

    connections = Connection.objects.filter(
        (Q(user=user) | Q(connection=user)), 
        status='accepted'
    )

    users = User.objects.filter(Q(id__in=connections.values('user')) | Q(id__in=connections.values('connection')))
    profiles = MainProfile.objects.filter(user__in=users).exclude(user=user)

    return render(request, 'connections/connections.html', {'profiles': profiles})

@login_required
def list_users(request):
    accepted_connections = Connection.objects.filter(Q(user=request.user) | Q(connection=request.user), status='accepted')
    pending_connections = Connection.objects.filter(Q(user=request.user) | Q(connection=request.user), status='pending')

    accepted_user_ids = set(accepted_connections.values_list('user', flat=True)) | set(accepted_connections.values_list('connection', flat=True))
    pending_user_ids = set(pending_connections.values_list('user', flat=True)) | set(pending_connections.values_list('connection', flat=True))
    
    all_excluded_users = accepted_user_ids | pending_user_ids

    users = User.objects.all().exclude(id=request.user.id).exclude(id__in=all_excluded_users)
    profiles = MainProfile.objects.filter(user__in=users)

    return render(request, 'connections/user_list.html', {'profiles': profiles})

@login_required
def pending_request(request):
    pending_connections = Connection.objects.filter(user=request.user, status='pending').values_list('connection', flat=True)
    users = User.objects.filter(id__in=pending_connections)
    profiles = MainProfile.objects.filter(user__in=users)

    return render(request, 'connections/pending_list.html', {'profiles': profiles})

@login_required
def send_connection_request(request, user_id):
    if request.method == 'POST':
        sender = request.user
        receiver = get_object_or_404(User, id=user_id)

        existing_request = Connection.objects.filter(
            (Q(user=sender, connection=receiver) | Q(user=receiver, connection=sender)), 
            status__in=['pending', 'accepted']
        ).exists()
        
        if existing_request:
            messages.error(request, "Connection request already exists.")
            return redirect('list_users')

        Connection.objects.create(user=sender, connection=receiver, status='pending')
        messages.success(request, "Connection request sent.")
        return redirect('list_users')
    else:
        return redirect('list_users')

@login_required
def incoming_requests(request):
    incoming_requests = Connection.objects.filter(connection=request.user, status='pending')
    
    profiles_with_con_ids = []
    for connection in incoming_requests:
        profile = MainProfile.objects.get(user=connection.user)
        profiles_with_con_ids.append({
            'profile': profile,
            'con_id': connection.id
        })
    
    return render(request, 'connections/incoming_list.html', {'profiles_with_con_ids': profiles_with_con_ids})

@login_required
def accept_connection_request(request, connection_id):
    if request.method == 'POST':
        for i in Connection.objects.all():
            print(i.id, i.connection, i.status, "||", connection_id, request.user)
        try:
            connection = Connection.objects.get(id=connection_id, connection=request.user, status='pending')
            connection.status = 'accepted'
            connection.save()
            messages.success(request, "Connection request accepted.")
        except Connection.DoesNotExist:
            print("Connection request does not exist")
            messages.error(request, "Connection request does not exist.")
        print("Acceted")
        return redirect('incoming_requests')
    else:
        print("invalid method")
        return redirect('incoming_requests')

@login_required
def reject_connection_request(request, connection_id):
    if request.method == 'POST':
        try:
            connection = Connection.objects.get(id=connection_id, connection=request.user, status='pending')
            connection.status = 'rejected'
            connection.save()
            messages.success(request, "Connection request rejected.")
        except Connection.DoesNotExist:
            messages.error(request, "Connection request does not exist.")
        return redirect('incoming_requests')
    else:
        return redirect('incoming_requests')
