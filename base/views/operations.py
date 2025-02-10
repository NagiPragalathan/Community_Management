from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from base.models import ChapterMemberPosition, MainProfile, Visitor, Chapter, ChapterGoles, ContactDetails
from django.http import HttpResponse
from django.core.mail import send_mail


@login_required
def visitor_registration_portal(request):
    visitors = Visitor.objects.filter(user=request.user).order_by('-date')
    return render(request, 'operations/list_visitor.html', {'visitors': visitors})

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
        members_data = []
        chapter_name = "No Chapter"
    else:
        # Get all members in the same chapter
        chapter_members = MainProfile.objects.filter(Chapter=chapter)
        
        # Get contact details for each member
        members_data = []
        for member in chapter_members:
            try:
                contact = ContactDetails.objects.get(user=member.user)
                members_data.append({
                    'name': f"{member.user.first_name} {member.user.last_name}",
                    'email': contact.email,
                    'phone': contact.phone,
                    'mobile': contact.mobile_number,
                    'website': contact.website
                })
            except ContactDetails.DoesNotExist:
                continue
        
        chapter_name = chapter.chapter_name
    
    context = {
        'members_data': members_data,
        'chapter_name': chapter_name,
        'member_count': len(members_data)
    }
    return render(request, 'operations/chapter_emails.html', context)


@login_required
def register_visitor(request, visitor_id=None):
    visitor = None
    if visitor_id:
        visitor = get_object_or_404(Visitor, id=visitor_id, user=request.user)
    
    if request.method == "POST":
        # Get form data
        data = {
            'user': request.user,
            'title': request.POST.get("title"),
            'first_name': request.POST.get("first_name"),
            'last_name': request.POST.get("last_name"),
            'suffix': request.POST.get("suffix"),
            'email': request.POST.get("email"),
            'phone_number': request.POST.get("phone_number"),
            'company_name': request.POST.get("company_name"),
            'address_line_1': request.POST.get("address_line_1"),
            'address_line_2': request.POST.get("address_line_2"),
            'city': request.POST.get("city"),
            'state_country_province': request.POST.get("state_country_province"),
            'post_code': request.POST.get("post_code"),
            'category': request.POST.get("category"),
            'visitor_type': request.POST.get("visitor_type"),
        }

        if visitor:
            # Update existing visitor
            for key, value in data.items():
                setattr(visitor, key, value)
            visitor.save()
            messages.success(request, "Visitor updated successfully!")
        else:
            # Create new visitor
            visitor = Visitor.objects.create(**data)
            messages.success(request, "Visitor registered successfully!")

        # Handle invitation email
        if request.POST.get("send_invitations"):
            send_mail(
                'Invitation to Visit',
                'You have been invited to visit our facility. Please contact us for further details.',
                'from@example.com',
                [data['email']],
                fail_silently=False,
            )

        return redirect('visitor_registration_portal')

    return render(request, "operations/Visitor_register.html", {'visitor': visitor})

@login_required
def delete_visitor(request, visitor_id):
    visitor = get_object_or_404(Visitor, id=visitor_id, user=request.user)
    visitor.delete()
    messages.success(request, "Visitor deleted successfully!")
    return redirect('visitor_registration_portal')

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
