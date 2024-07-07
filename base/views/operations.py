from django.shortcuts import render

def visitor_registration_portal(request):
    return render(request, 'visitor_registration_portal.html')

def view_palms_summary(request):
    return render(request, 'view_palms_summary.html')

def view_chapter_goals(request):
    return render(request, 'view_chapter_goals.html')

def email_my_chapter(request):
    return render(request, 'email_my_chapter.html')

def email_visitor_invitation(request):
    return render(request, 'email_visitor_invitation.html')

def email_chapter_visitors(request):
    return render(request, 'email_chapter_visitors.html')

def manage_news(request):
    return render(request, 'manage_news.html')

def operations(request):
    return render(request, 'operations/operations.html')

# Define other views as needed
