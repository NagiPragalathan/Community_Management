from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from base.models import ChapterEducationUnit, User
from django.utils.timezone import now

@login_required
def create_ceu(request):
    if request.method == 'POST':
        course_title = request.POST.get('course_title')
        credits_per_course = request.POST.get('credits_per_course')
        qty_earned = request.POST.get('qty_earned')
        
        ChapterEducationUnit.objects.create(
            user=request.user,
            date=now(),
            course_title=course_title,
            credits_per_course=credits_per_course,
            qty_earned=qty_earned,
            total_credits_last_week=0  # Assuming some logic to calculate this
        )
        return redirect('review_ceu')
    
    return render(request, 'ceus/create_ceu.html')

@login_required
def review_ceu(request):
    ceus = ChapterEducationUnit.objects.filter(user=request.user)
    return render(request, 'ceus/review_ceu.html', {'ceus': ceus})
