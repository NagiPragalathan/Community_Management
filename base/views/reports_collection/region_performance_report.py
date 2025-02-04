from django.shortcuts import render
from django.db.models import Sum
from base.models import Chapter, MainProfile, Visitor, ReferralSlip, TYFCB, Region
from base.views.common import calculate_meeting_counts, calculate_ceu_counts
from datetime import datetime

def region_performance_report(request):
    regions = Region.objects.all()
    selected_from_date = None
    selected_to_date = None
    region_data = []

    if request.method == 'POST':
        selected_from_date = request.POST.get('from_date')
        selected_to_date = request.POST.get('to_date')

        if selected_from_date and selected_to_date:
            # Convert string dates to datetime objects
            from_date = datetime.strptime(selected_from_date, "%Y-%m-%d").date()
            to_date = datetime.strptime(selected_to_date, "%Y-%m-%d").date()

            for region in regions:
                # Get all chapters in the region
                chapters_in_region = Chapter.objects.filter(region=region)

                # Extract the ChapterName objects from chapters_in_region
                chapter_names_in_region = chapters_in_region.values_list('name', flat=True)

                # Get all members in the region (members in the chapters)
                members_in_region = MainProfile.objects.filter(Chapter__in=chapter_names_in_region)

                # Extract user IDs from MainProfile
                user_list = members_in_region.values_list('user', flat=True)

                # Aggregate Data for the Region
                one_to_one_count = sum(calculate_meeting_counts(m.user)[1] for m in members_in_region)
                ceu_count = sum(calculate_ceu_counts(m.user)[1] for m in members_in_region)

                visitor_count = Visitor.objects.filter(user__in=user_list, date__range=[from_date, to_date]).count()
                tyfcb_count = TYFCB.objects.filter(user__in=user_list, start_date__range=[from_date, to_date]).count()
                tyfcb_received_count = TYFCB.objects.filter(thank_you_to__in=user_list, start_date__range=[from_date, to_date]).count()
                tyfcb_given_count = TYFCB.objects.filter(user__in=user_list, start_date__range=[from_date, to_date]).count()

                referral_received_count = ReferralSlip.objects.filter(to_member__in=user_list, date__range=[from_date, to_date]).count()
                referral_given_count = ReferralSlip.objects.filter(from_user__in=user_list, date__range=[from_date, to_date]).count()

                # Store consolidated data for the region
                region_data.append({
                    'region_name': region.region_name,
                    'one_to_one_count': one_to_one_count,
                    'ceu_count': ceu_count,
                    'visitor_count': visitor_count,
                    'tyfcb_count': tyfcb_count,
                    'tyfcb_received_count': tyfcb_received_count,
                    'tyfcb_given_count': tyfcb_given_count,
                    'referral_received_count': referral_received_count,
                    'referral_given_count': referral_given_count,
                })

    return render(request, 'reports/region_performance_report/region_performance_report.html', {
        'regions': regions,
        'region_data': region_data,
        'selected_from_date': selected_from_date,
        'selected_to_date': selected_to_date
    })
