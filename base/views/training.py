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
        TrainingSession.objects.create(training_name=training_name, date=date)
        return redirect('list_training_sessions')
    
    return render(request, 'training_sessions/create.html')


def edit_training_session(request, pk):
    session = get_object_or_404(TrainingSession, pk=pk)
    
    if request.method == 'POST':
        session.training_name = request.POST.get('training_name')
        session.date = request.POST.get('date')
        session.save()
        return redirect('list_training_sessions')

    return render(request, 'training_sessions/edit.html', {'session': session})

def delete_training_session(request, pk):
    session = get_object_or_404(TrainingSession, pk=pk)
    session.delete()
    return redirect('list_training_sessions')
