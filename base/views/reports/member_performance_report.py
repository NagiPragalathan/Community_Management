from django.shortcuts import render, redirect
from django.http import JsonResponse
from base.models import Chapter, MainProfile, PAS, ChapterName
from datetime import datetime

def member_performance_report(request):
    # Get all chapters for the dropdown
    chapters = Chapter.objects.all()

    selected_chapter = None
    selected_date = None
    members = []

    if request.method == 'POST':
        if 'chapter' in request.POST:
            selected_chapter_id = request.POST.get('chapter')
            selected_chapter = Chapter.objects.get(id=selected_chapter_id)
            selected_date = request.POST.get('date')

            chapter_name = selected_chapter.name
            
            members = MainProfile.objects.filter(Chapter=chapter_name)
            for i in members:
                try:
                    attendance_records = PAS.objects.get(user=i,chapter=Chapter.objects.get(name=chapter_name), date=selected_date)
                    i.attendance_records = attendance_records
                except:
                    i.attendance_records = None
                    print("not found")

    return render(request, 'reports/member_performance/member_performance_report.html', {
        'chapters': chapters,
        'selected_chapter': selected_chapter,
        'members': members,
        'selected_date': selected_date
    })