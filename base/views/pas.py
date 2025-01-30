from django.shortcuts import render, redirect
from django.http import JsonResponse
from base.models import Chapter, MainProfile, PAS, ChapterName
from datetime import datetime


def chapter_members(request):
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

    return render(request, 'pas/chapter_members.html', {
        'chapters': chapters,
        'selected_chapter': selected_chapter,
        'members': members,
        'selected_date': selected_date
    })


def update_attendance(request):
    if request.method == 'POST':
        # Retrieve the chapter and date from the form
        selected_chapter_id = request.POST.get('chapter_id')
        date_str = request.POST.get('date')  # Make sure this is in 'YYYY-MM-DD' format

        # Validate that the date is in the correct format
        try:
            # Try to parse the date to ensure it's in the correct format
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            # If the date format is wrong, raise an error or return a response with an error message
            return JsonResponse({'error': 'Invalid date format. It must be in YYYY-MM-DD format.'})

        # Get the selected chapter
        selected_chapter = Chapter.objects.get(id=selected_chapter_id)
        print(selected_chapter, "working..!")

        # Loop through the members and save their attendance
        for member in MainProfile.objects.filter(Chapter=selected_chapter.name):
            attendance_status = request.POST.get(f'attendance_{member.id}')
            if attendance_status:
                # Check if the PAS entry already exists
                pas_entry, created = PAS.objects.get_or_create(
                    user=member,
                    chapter=selected_chapter,
                    date=date,
                    defaults={
                        'present': (attendance_status == 'present'),
                        'absent': (attendance_status == 'absent')
                    }
                )
                if not created:
                    pas_entry.present = (attendance_status == 'present')
                    pas_entry.absent = (attendance_status == 'absent')
                    pas_entry.save()
                print(attendance_status)

        return redirect('chapter_members')  # Redirect to chapter members page after submission

    return JsonResponse({'status': 'error'})
