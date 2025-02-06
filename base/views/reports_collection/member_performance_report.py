from django.shortcuts import render
from base.models import Chapter, MainProfile, Visitor, ReferralSlip, TYFCB, PAS
from base.views.common import calculate_meeting_counts, calculate_ceu_counts
from django.utils import timezone
from datetime import datetime


def is_admin_user(user):
    """
    Check if the user is a superuser or has staff permissions
    """
    return user.is_superuser or user.is_staff


def member_performance_report(request):
    chapters = Chapter.objects.all()
    selected_chapter = None
    selected_from_date = None
    selected_to_date = None
    members = []

    if request.method == 'POST':
        selected_chapter_id = request.POST.get('chapter')
        selected_from_date = request.POST.get('from_date')
        selected_to_date = request.POST.get('to_date')

        if selected_chapter_id and selected_from_date and selected_to_date:
            selected_chapter = Chapter.objects.get(id=selected_chapter_id)
            chapter_name = selected_chapter.name
            members = MainProfile.objects.filter(Chapter=chapter_name)

            # Convert string dates to datetime objects
            from_date = datetime.strptime(selected_from_date, "%Y-%m-%d").date()
            to_date = datetime.strptime(selected_to_date, "%Y-%m-%d").date()

            for i in members:
                # One-to-One Meetings
                _, last_12_months_count, _ = calculate_meeting_counts(i.user)
                i.onelast_12_months_count = last_12_months_count

                # CEU
                _, last_12_months_count, _ = calculate_ceu_counts(i.user)
                i.eculast_12_months_count = last_12_months_count

                # Visitor Counts
                visitor_count = Visitor.objects.filter(user=i.user, date__range=[from_date, to_date]).count()
                i.visitor_count = visitor_count

                # TYFCB Counts
                tyfcb_count = TYFCB.objects.filter(user=i.user, start_date__range=[from_date, to_date]).count()
                i.tyfcb_count = tyfcb_count

                # TYFCB Received
                tyfcb_received_count = TYFCB.objects.filter(thank_you_to=i.user, start_date__range=[from_date, to_date]).count()
                i.tyfcb_received_count = tyfcb_received_count

                # TYFCB Given
                tyfcb_given_count = TYFCB.objects.filter(user=i.user, start_date__range=[from_date, to_date]).count()
                i.tyfcb_given_count = tyfcb_given_count

                # Referrals Received
                referral_received_count = ReferralSlip.objects.filter(to_member=i.user, date__range=[from_date, to_date]).count()
                i.referral_received_count = referral_received_count

                # Referrals Given
                referral_given_count = ReferralSlip.objects.filter(from_user=i.user, date__range=[from_date, to_date]).count()
                i.referral_given_count = referral_given_count

                # ✅ PAS Attendance
                present_count = PAS.objects.filter(user=i, date__range=[from_date, to_date], present=True).count()
                absent_count = PAS.objects.filter(user=i, date__range=[from_date, to_date], absent=True).count()
                i.present_count = present_count
                i.absent_count = absent_count

    return render(request, 'reports/member_performance/member_performance_report.html', {
        'chapters': chapters,
        'selected_chapter': selected_chapter,
        'members': members,
        'selected_from_date': selected_from_date,
        'selected_to_date': selected_to_date,
        'base_template': 'admin_base.html' if is_admin_user(request.user) else 'base.html' 
    })
