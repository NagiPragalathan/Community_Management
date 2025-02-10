from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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
    ceus = ChapterEducationUnit.objects.filter(user=request.user).order_by('-date')
    return render(request, 'ceus/review_ceu.html', {'ceus': ceus})

@login_required
def edit_ceu(request, ceu_id):
    ceu = get_object_or_404(ChapterEducationUnit, id=ceu_id, user=request.user)
    
    if request.method == 'POST':
        ceu.course_title = request.POST.get('course_title')
        ceu.credits_per_course = request.POST.get('credits_per_course')
        ceu.qty_earned = request.POST.get('qty_earned')
        ceu.save()
        messages.success(request, 'CEU updated successfully!')
        return redirect('review_ceu')
    
    return render(request, 'ceus/edit_ceu.html', {'ceu': ceu})

@login_required
def delete_ceu(request, ceu_id):
    ceu = get_object_or_404(ChapterEducationUnit, id=ceu_id, user=request.user)
    if request.method == 'POST':
        ceu.delete()
        messages.success(request, 'CEU deleted successfully!')
        return redirect('review_ceu')
    return render(request, 'ceus/delete_ceu.html', {'ceu': ceu})
