from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from base.models import oneToOneMessage
from django.http import JsonResponse
from django.db.models import Q
from operator import attrgetter
from collections import defaultdict

@login_required
def chat_view(request, receiver_id):
    receiver = User.objects.get(pk=receiver_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        oneToOneMessage.objects.create(sender=request.user, receiver=receiver, content=content)
        return redirect('chat', receiver_id=receiver_id)

    receiver = User.objects.get(pk=receiver_id)
    messages = oneToOneMessage.objects.filter(sender=request.user, receiver=receiver) | \
               oneToOneMessage.objects.filter(sender=receiver, receiver=request.user)
    messages = messages.order_by('timestamp')
    print(receiver, receiver.id, receiver.username)
    # Mark existing unseen messages as seen
    unseen_messages = oneToOneMessage.objects.filter(sender=receiver, receiver=request.user, seen=False)
    unseen_messages.update(seen=True)
    return render(request, 'chat/chat.html', {'receiver': receiver, 'messages': messages, 'receiver_id':receiver_id})

@login_required
def update_message(request, receiver_id):
    if request.method == 'POST':
        receiver = User.objects.get(pk=receiver_id)
        content = request.POST.get('content')
        
        # Create a new message
        new_message = oneToOneMessage.objects.create(sender=request.user, receiver=receiver, content=content)
        
        # Mark existing unseen messages as seen
        unseen_messages = oneToOneMessage.objects.filter(sender=receiver, receiver=request.user, seen=False)
        unseen_messages.update(seen=True)
        
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})
    

@login_required
def one_to_one_get_messages(request, receiver_id):
    try:
        receiver = User.objects.get(pk=receiver_id)
        # Fetch messages from both sender and receiver
        messages = oneToOneMessage.objects.filter(Q(sender=receiver, receiver=request.user) | Q(sender=request.user, receiver=receiver))
        # Sort messages by timestamp
        sorted_messages = sorted(messages, key=attrgetter('timestamp'))
        message_list = [{'sender': msg.sender.username, 'content': msg.content, 'timestamp': msg.timestamp} for msg in sorted_messages]
        return JsonResponse({'status': 'success', 'messages': message_list})
    except User.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Receiver not found'})

@login_required
def unseen_messages(request):
    current_user = request.user
    
    # Fetch all unseen messages for the current user
    unseen_messages = oneToOneMessage.objects.filter(receiver=current_user, seen=False)
    
    # Group messages by sender
    unseen_messages_per_user = defaultdict(list)
    for message in unseen_messages:
        unseen_messages_per_user[message.sender].append(message)

    return render(request, 'chat/unseen_messages.html', {'unseen_messages_per_user': dict(unseen_messages_per_user)})
