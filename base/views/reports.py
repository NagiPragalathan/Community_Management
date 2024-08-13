from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import JsonResponse
from base.models import Chapter, TrainingSession, MainProfile

def training_session_list(request):
    sessions = TrainingSession.objects.all()
    return render(request, 'reports/training_session_list.html', {'sessions': sessions})

def add_training_session(request):
    if request.method == 'POST':
        training_name = request.POST.get('training_name')
        date = request.POST.get('date')
        chapter_id = request.POST.get('chapter')
        attendees = request.POST.getlist('attendees')

        if chapter_id == 'all':
            chapter = None
        else:
            chapter = Chapter.objects.get(id=chapter_id)
        
        session = TrainingSession.objects.create(
            training_name=training_name,
            date=date,
            chapter=chapter,
        )
        session.attendees.set(User.objects.filter(id__in=attendees))
        return redirect('training_session_list')

    chapters = Chapter.objects.all()
    return render(request, 'reports/add_training_session.html', {'chapters': chapters})

def get_chapter_users(request):
    chapter_id = request.GET.get('chapter_id')
    if chapter_id == 'all':
        users = User.objects.all().values('id', 'username')
    else:
        users = User.objects.filter(mainprofile__Chapter_id=chapter_id).values('id', 'username')
    return JsonResponse({'users': list(users)})
