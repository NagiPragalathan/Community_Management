from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from base.models import ChapterMemberPosition, MainProfile, Visitor
from django.http import HttpResponse


def visitor_registration_portal(request):
    return render(request, 'visitor_registration_portal.html')

def view_palms_summary(request):
    return render(request, 'view_palms_summary.html')

def view_chapter_goals(request):
    return render(request, 'view_chapter_goals.html')

def email_my_chapter(request):
    return render(request, 'email_my_chapter.html')

def send_invitation_view(request):
    if request.method == 'POST':
        # Process the form data
        # You might want to send an email here
        return redirect('some_success_url')  # Redirect after POST
    return render(request, 'email/email_visitor_invitation.html')

def email_chapter_visitors(request):
    return render(request, 'email_chapter_visitors.html')

def manage_news(request):
    return render(request, 'manage_news.html')

def operations(request):
    return render(request, 'operations/operations.html')

def user_chapter_emails(request):
    # Get the current user's MainProfile
    main_profile = get_object_or_404(MainProfile, user=request.user)
    
    # Get the chapter of the current user
    chapter = main_profile.Chapter
    
    # Check if the user is in a chapter
    if not chapter:
        emails = []
        chapter_name = "No Chapter"
    else:
        # Get all members in the same chapter
        chapter_members = MainProfile.objects.filter(Chapter=chapter)
        
        # Get all email IDs of the chapter members
        emails = [member.user.email for member in chapter_members]
        chapter_name = chapter.chapter_name
    
    # Render the emails in the HTML template
    context = {'emails': emails, 'chapter_name': chapter_name}
    return render(request, 'operations/chapter_emails.html', context)



@login_required
def register_visitor(request):
    if request.method == "POST":
        title = request.POST.get("title")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        suffix = request.POST.get("suffix")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        company_name = request.POST.get("company_name")
        address_line_1 = request.POST.get("address_line_1")
        address_line_2 = request.POST.get("address_line_2")
        city = request.POST.get("city")
        state_country_province = request.POST.get("state_country_province")
        post_code = request.POST.get("post_code")
        category = request.POST.get("category")
        visitor_type = request.POST.get("visitor_type")

        visitor = Visitor(
            user=request.user,
            title=title,
            first_name=first_name,
            last_name=last_name,
            suffix=suffix,
            email=email,
            phone_number=phone_number,
            company_name=company_name,
            address_line_1=address_line_1,
            address_line_2=address_line_2,
            city=city,
            state_country_province=state_country_province,
            post_code=post_code,
            category=category,
            visitor_type=visitor_type,
        )
        visitor.save()
        return HttpResponse("Registration successful")

    return render(request, "operations/Visitor_register.html")
