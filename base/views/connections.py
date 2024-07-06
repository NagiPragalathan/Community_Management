from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from base.models import Connection, MainProfile
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

from django.db.models import Q

@login_required
def connection_list(request):
    connections = Connection.objects.filter(
        Q(user=request.user) | Q(connection=request.user), 
        status='accepted'
    )
    users = User.objects.filter(id__in=connections)
    profiles = MainProfile.objects.filter(user__in=users)

    return render(request, 'connections/connections.html', {'profiles': profiles})

@login_required
def list_users(request):
    # Get the current user's accepted and pending connections
    accepted_connections = Connection.objects.filter(user=request.user, status='accepted').values_list('connection', flat=True)
    pending_connections = Connection.objects.filter(user=request.user, status='pending').values_list('connection', flat=True)
    
    # Get users who have accepted the current user's connection request
    accepted_by_others = Connection.objects.filter(connection=request.user, status='accepted').values_list('user', flat=True)
    pending_by_others = Connection.objects.filter(connection=request.user, status='pending').values_list('user', flat=True)
    
    all_excluded_users = set(accepted_connections) | set(pending_connections) | set(accepted_by_others) | set(pending_by_others)
    
    # Filter users excluding the current user and all excluded users
    users = User.objects.all().exclude(id=request.user.id).exclude(id__in=all_excluded_users)
    
    profiles = MainProfile.objects.filter(user__in=users)

    return render(request, 'connections/user_list.html', {'profiles': profiles})


@login_required
def pending_request(request):
    pending_connections = Connection.objects.filter(user=request.user, status='pending').values_list('connection', flat=True)
    users = User.objects.filter(id__in=pending_connections)
    profiles = MainProfile.objects.filter(user__in=users)

    return render(request, 'connections/pending_list.html', {'profiles': profiles})


def send_connection_request(request, user_id):
    print("req:", request.method)
    if request.method == 'GET':
        sender = request.user
        receiver = get_object_or_404(User, id=user_id)
        print("working")
        # Check if a connection request already exists
        existing_request = Connection.objects.filter(user=sender, connection=receiver, status__in=['pending', 'accepted']).exists()
        if existing_request:
            # Handle case where request already exists
            print("Connection request already exists.")
            return redirect('list_users')

        # Create a new connection request
        connection_request = Connection(user=sender, connection=receiver, status='pending')
        connection_request.save()
        
        print("Connection request sent.", connection_request.id)
        
        return redirect('list_users')
    else:
        return redirect('list_users')


def incoming_requests(request):
    incoming_requests = Connection.objects.filter(connection=request.user, status='pending')
    profiles = MainProfile.objects.filter(user__in=[req.user for req in incoming_requests])
    return render(request, 'connections/incoming_list.html', {'profiles': profiles})


def accept_connection_request(request, connection_id):
    if request.method == 'POST':
        connection = Connection.objects.get(id=connection_id)
        connection.status = 'accepted'
        connection.save()
        print("Connection request accepted.")
        return redirect('list_users')
    else:
        return redirect('list_users')

def reject_connection_request(request, connection_id):
    if request.method == 'POST':
        connection = Connection.objects.get(id=connection_id)
        connection.status = 'rejected'
        connection.save()
        print("Connection request rejected.")
        return redirect('list_users')
    else:
        return redirect('list_users')
