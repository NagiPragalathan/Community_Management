from django.shortcuts import render
from django.db.models import Sum
from base.models import Chapter, MainProfile, Visitor, ReferralSlip, TYFCB
from base.views.common import calculate_meeting_counts, calculate_ceu_counts
from datetime import datetime


def chapter_performance_report(request):
    chapters = Chapter.objects.all()
    selected_from_date = None
    selected_to_date = None
    chapter_data = []

    if request.method == 'POST':
        selected_from_date = request.POST.get('from_date')
        selected_to_date = request.POST.get('to_date')

        if selected_from_date and selected_to_date:
            # Convert string dates to datetime objects
            from_date = datetime.strptime(selected_from_date, "%Y-%m-%d").date()
            to_date = datetime.strptime(selected_to_date, "%Y-%m-%d").date()

            for chapter in chapters:
                # Get all members in the chapter
                members = MainProfile.objects.filter(Chapter=chapter.name)

                # Extract user IDs from MainProfile
                user_list = members.values_list('user', flat=True)

                # Aggregate Data for the Chapter
                one_to_one_count = sum(calculate_meeting_counts(m.user)[1] for m in members)
                ceu_count = sum(calculate_ceu_counts(m.user)[1] for m in members)

                visitor_count = Visitor.objects.filter(user__in=user_list, date__range=[from_date, to_date]).count()
                tyfcb_count = TYFCB.objects.filter(user__in=user_list, start_date__range=[from_date, to_date]).count()
                tyfcb_received_count = TYFCB.objects.filter(thank_you_to__in=user_list, start_date__range=[from_date, to_date]).count()
                tyfcb_given_count = TYFCB.objects.filter(user__in=user_list, start_date__range=[from_date, to_date]).count()

                referral_received_count = ReferralSlip.objects.filter(to_member__in=user_list, date__range=[from_date, to_date]).count()
                referral_given_count = ReferralSlip.objects.filter(from_user__in=user_list, date__range=[from_date, to_date]).count()

                # Store consolidated data for the chapter
                chapter_data.append({
                    'chapter_name': chapter.name.chapter_name,
                    'one_to_one_count': one_to_one_count,
                    'ceu_count': ceu_count,
                    'visitor_count': visitor_count,
                    'tyfcb_count': tyfcb_count,
                    'tyfcb_received_count': tyfcb_received_count,
                    'tyfcb_given_count': tyfcb_given_count,
                    'referral_received_count': referral_received_count,
                    'referral_given_count': referral_given_count,
                })

    return render(request, 'reports/chapter_performance_report/chapter_performance_report.html', {
        'chapters': chapters,
        'chapter_data': chapter_data,
        'selected_from_date': selected_from_date,
        'selected_to_date': selected_to_date
    })
