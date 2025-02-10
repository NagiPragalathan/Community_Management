from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from base.models import Meeting, User
from django.db.models import Q 

@login_required
def create_meeting(request):
    if request.method == 'POST':
        met_with_id = request.POST.get('met_with')
        invited_by = request.user  # Automatically set to the current logged-in user
        location = request.POST.get('location')
        topics_of_conversation = request.POST.get('topics_of_conversation')
        date = request.POST.get('date')

        met_with = User.objects.get(id=met_with_id)

        Meeting.objects.create(
            met_with=met_with,
            invited_by=invited_by,
            location=location,
            topics_of_conversation=topics_of_conversation,
            date=date
        )
        return redirect('meeting_list')  # Assuming you have a URL named 'meeting_list'

    users = User.objects.all()  # Fetching all users to display in the dropdown
    return render(request, 'oneslip/create_meeting.html', {'users': users})

@login_required
def meeting_list(request):
    meetings = Meeting.objects.filter(invited_by=request.user)
    return render(request, 'oneslip/meeting_list.html', {'meetings': meetings})

@login_required
def one_to_one_list(request):
    # Fetch meetings where the current user is either the person they met with or the one who invited
    meetings = Meeting.objects.filter(Q(met_with=request.user) | Q(invited_by=request.user)).distinct()
    return render(request, 'oneslip/one_to_one_list.html', {'meetings': meetings})

@login_required
def edit_meeting(request, meeting_id):
    meeting = Meeting.objects.get(id=meeting_id)
    
    # Check if user has permission to edit
    if meeting.invited_by != request.user:
        return redirect('meeting_list')
        
    if request.method == 'POST':
        met_with_id = request.POST.get('met_with')
        location = request.POST.get('location')
        topics_of_conversation = request.POST.get('topics_of_conversation')
        date = request.POST.get('date')

        meeting.met_with = User.objects.get(id=met_with_id)
        meeting.location = location
        meeting.topics_of_conversation = topics_of_conversation
        meeting.date = date
        meeting.save()
        
        return redirect('meeting_list')

    users = User.objects.all()
    return render(request, 'oneslip/edit_meeting.html', {
        'meeting': meeting,
        'users': users
    })

@login_required
def delete_meeting(request, meeting_id):
    meeting = Meeting.objects.get(id=meeting_id)
    
    # Check if user has permission to delete
    if meeting.invited_by == request.user:
        meeting.delete()
    
    return redirect('meeting_list')


