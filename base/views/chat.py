from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from base.models import Message
from django.http import JsonResponse
from django.db.models import Q
from operator import attrgetter

@login_required
def chat_view(request, receiver_id):
    if request.method == 'POST':
        receiver = User.objects.get(pk=receiver_id)
        content = request.POST.get('content')
        Message.objects.create(sender=request.user, receiver=receiver, content=content)
        return redirect('chat', receiver_id=receiver_id)

    receiver = User.objects.get(pk=receiver_id)
    messages = Message.objects.filter(sender=request.user, receiver=receiver) | \
               Message.objects.filter(sender=receiver, receiver=request.user)
    messages = messages.order_by('timestamp')
    print(receiver, receiver.id, receiver.username)
    # Mark existing unseen messages as seen
    unseen_messages = Message.objects.filter(sender=receiver, receiver=request.user, seen=False)
    unseen_messages.update(seen=True)
    return render(request, 'chat/chat.html', {'receiver': receiver, 'messages': messages, 'receiver_id':receiver_id})

@login_required
def update_message(request, receiver_id):
    if request.method == 'POST':
        receiver = User.objects.get(pk=receiver_id)
        content = request.POST.get('content')
        
        # Create a new message
        new_message = Message.objects.create(sender=request.user, receiver=receiver, content=content)
        
        # Mark existing unseen messages as seen
        unseen_messages = Message.objects.filter(sender=receiver, receiver=request.user, seen=False)
        unseen_messages.update(seen=True)
        
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})
    

@login_required
def get_messages(request, receiver_id):
    try:
        receiver = User.objects.get(pk=receiver_id)
        # Fetch messages from both sender and receiver
        messages = Message.objects.filter(Q(sender=receiver, receiver=request.user) | Q(sender=request.user, receiver=receiver))
        # Sort messages by timestamp
        sorted_messages = sorted(messages, key=attrgetter('timestamp'))
        message_list = [{'sender': msg.sender.username, 'content': msg.content, 'timestamp': msg.timestamp} for msg in sorted_messages]
        return JsonResponse({'status': 'success', 'messages': message_list})
    except User.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Receiver not found'})

def unseen_messages(request):
    current_user = request.user
    unseen_messages_per_user = {}
    for user in User.objects.exclude(id=current_user.id):
        unseen_messages = Message.objects.filter(receiver=current_user, sender=user, seen=False)
        unseen_messages_per_user[user] = unseen_messages
    print("working..!")
    return render(request, 'chat/unseen_messages.html', {'unseen_messages_per_user': unseen_messages_per_user})

