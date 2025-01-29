from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from base.models import TrainingSession, Chapter
from django.urls import reverse

def list_training_sessions(request):
    sessions = TrainingSession.objects.all()
    return render(request, 'training_sessions/list.html', {'sessions': sessions})

def create_training_session(request):
    if request.method == 'POST':
        training_name = request.POST.get('training_name')
        date = request.POST.get('date')
        chapter_id = request.POST.get('chapter')
        chapter = get_object_or_404(Chapter, id=chapter_id)
        TrainingSession.objects.create(training_name=training_name, date=date, chapter=chapter)
        return redirect('list_training_sessions')
    
    chapters = Chapter.objects.all()
    return render(request, 'training_sessions/create.html', {'chapters': chapters})

def edit_training_session(request, pk):
    session = get_object_or_404(TrainingSession, pk=pk)
    
    if request.method == 'POST':
        session.training_name = request.POST.get('training_name')
        session.date = request.POST.get('date')
        session.chapter = get_object_or_404(Chapter, id=request.POST.get('chapter'))
        session.save()
        return redirect('list_training_sessions')

    chapters = Chapter.objects.all()
    return render(request, 'training_sessions/edit.html', {'session': session, 'chapters': chapters})

def delete_training_session(request, pk):
    session = get_object_or_404(TrainingSession, pk=pk)
    session.delete()
    return redirect('list_training_sessions')
