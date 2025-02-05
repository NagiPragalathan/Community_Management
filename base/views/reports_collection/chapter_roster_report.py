from django.shortcuts import render
from base.models import Chapter, MainProfile, ContactDetails

def chapter_roster_report(request):
    # Get all chapters
    chapters = Chapter.objects.all()
    selected_chapter = None
    members_in_chapter = []
    selected_chapter_name = None

    if request.method == 'POST':
        selected_chapter = request.POST.get('chapter')
        
        if selected_chapter:
            # Get the selected chapter object
            chapter = Chapter.objects.get(id=selected_chapter)
            selected_chapter_name = chapter.name.chapter_name  # Get the name of the selected chapter
            
            # Get the ChapterName object from the selected chapter
            chapter_name_instance = chapter.name  # The related ChapterName object

            # Get all members in the selected chapter along with their contact details
            members_in_chapter = MainProfile.objects.filter(Chapter=chapter_name_instance).select_related('user')
            
            # Optionally, fetch contact details related to each user
            for member in members_in_chapter:
                # Fetch the associated contact details for each member
                member.contact_details = ContactDetails.objects.filter(user=member.user).first()

    return render(request, 'reports/chapter_roster_report/chapter_roster_report.html', {
        'chapters': chapters,
        'selected_chapter': selected_chapter,
        'selected_chapter_name': selected_chapter_name,
        'members_in_chapter': members_in_chapter
    })
