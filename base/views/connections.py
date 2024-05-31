from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from base.models import Connection, MainProfile
from django.contrib.auth.models import User


@login_required
def accept_connection_request(request, connection_id):
    connection_request = Connection.objects.get(id=connection_id)
    connection_request.status = 'accepted'
    connection_request.save()
    return redirect('connection_list')

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

@login_required
def connection_list(request):
    connections = Connection.objects.filter(user=request.user, status='accepted')
    return render(request, 'connections/connections.html', {'connections': connections})


def list_users(request):
    # Get the current user's accepted and pending connections
    accepted_connections = Connection.objects.filter(user=request.user, status='accepted').values_list('connection', flat=True)
    pending_connections = Connection.objects.filter(user=request.user, status='pending').values_list('connection', flat=True)

    # Filter users excluding the current user and their accepted and pending connections
    users = User.objects.exclude(id=request.user.id).exclude(id__in=accepted_connections)
    for i in users:
        if i.id  in pending_connections:
            i.status = 'pending'
        else:
            i.status = 'none'
    profiles = MainProfile.objects.filter(user__in=users)
            
    return render(request, 'connections/user_list.html', {'profiles': profiles})

def send_connection_request(request, user_id):
    print("req:", request.method)
    if request.method == 'GET':
        sender = request.user
        receiver = User.objects.get(id=user_id)
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
        
        print("Connection request sent.")
        
        return redirect('list_users')
    else:
        return redirect('list_users')


def incoming_requests(request):
    # Get incoming connection requests for the current user
    incoming_requests = Connection.objects.filter(connection=request.user, status='pending')

    # Render the template with the incoming requests queryset
    return render(request, 'connections/incoming_requests.html', {'incoming_requests': incoming_requests})

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
