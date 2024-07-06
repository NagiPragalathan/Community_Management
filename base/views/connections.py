from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from base.models import Connection, MainProfile
from django.contrib.auth.models import User
import logging
from django.shortcuts import get_object_or_404, redirect

logger = logging.getLogger(__name__)

@login_required
def accept_connection_request(request, connection_id):
    connection_request = get_object_or_404(Connection, id=connection_id)
    
    if connection_request.status != 'pending':
        logger.error(f"Connection with id {connection_id} is not pending.")
        return redirect('incoming_requests')
    
    connection_request.status = 'accepted'
    connection_request.save()

    # Create a reciprocal connection
    reciprocal_connection, created = Connection.objects.get_or_create(
        user=connection_request.connection,
        connection=connection_request.user,
        defaults={'status': 'accepted'}
    )
    if not created:
        reciprocal_connection.status = 'accepted'
        reciprocal_connection.save()
    
    logger.info(f"Connection request accepted for connection id {connection_id}.")
    return redirect('connection_list')

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

@login_required
def connection_list(request):
    connections = Connection.objects.filter(user=request.user, status='accepted')
    return render(request, 'connections/connections.html', {'connections': connections})


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
        
        print("Connection request sent.")
        
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
