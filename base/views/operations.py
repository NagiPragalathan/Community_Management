from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from base.models import ChapterMemberPosition, MainProfile, Visitor, Chapter, ChapterGoles
from django.http import HttpResponse
from django.core.mail import send_mail


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
        send_invitations = request.POST.get("send_invitations")

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

        if send_invitations:
            send_mail(
                'Invitation to Visit',
                'You have been invited to visit our facility. Please contact us for further details.',
                'from@example.com',
                [email],
                fail_silently=False,
            )

        return HttpResponse("Registration successful")

    return render(request, "operations/Visitor_register.html")

@login_required
def set_goals(request):
    if request.method == 'POST':
        chapter_id = request.POST.get('chapter_id')
        chapter = Chapter.objects.get(id=chapter_id)

        attendance_percentage = request.POST.get('attendance_percentage')
        total_number_of_1_to_1s = request.POST.get('total_number_of_1_to_1s')
        ceus = request.POST.get('ceus')
        visitors = request.POST.get('visitors')
        new_memberships = request.POST.get('new_memberships')
        number_of_members_in_chapter = request.POST.get('number_of_members_in_chapter')
        number_of_referrals = request.POST.get('number_of_referrals')
        thank_you_for_closed_business = request.POST.get('thank_you_for_closed_business')
        date_of_month = request.POST.get('date_of_month')

        ChapterGoles.objects.create(
            user=request.user,
            chapter=chapter,
            attendance_percentage=attendance_percentage,
            total_number_of_1_to_1s=total_number_of_1_to_1s,
            ceus=ceus,
            visitors=visitors,
            new_memberships=new_memberships,
            number_of_members_in_chapter=number_of_members_in_chapter,
            number_of_referrals=number_of_referrals,
            thank_you_for_closed_business=thank_you_for_closed_business,
            date_of_month=date_of_month
        )

        return redirect('goals_list')

    chapters = Chapter.objects.all()
    return render(request, 'goals/set_goals.html', {'chapters': chapters})

@login_required
def goals_list(request):
    goals = ChapterGoles.objects.filter(user=request.user)
    return render(request, 'goals/goals_list.html', {'goals': goals})
