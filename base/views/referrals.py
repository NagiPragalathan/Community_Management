from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from base.models import ReferralSlip, User
from django.utils.dateparse import parse_date
from base.models import ReferralSlip
from django.db.models import Q

@login_required
def create_referral(request):
    if request.method == 'POST':
        to_member_id = request.POST.get('to_member')
        referral_description = request.POST.get('referral')
        referral_type = request.POST.get('referral_type')
        referral_status = request.POST.get('referral_status')
        address = request.POST.get('address', '')
        telephone = request.POST.get('telephone')
        email = request.POST.get('email', '')
        comments = request.POST.get('comments', '')
        referral_heat = request.POST.get('referral_heat')

        try:
            to_member = User.objects.get(id=to_member_id)
        except User.DoesNotExist:
            messages.error(request, "Selected member does not exist.")
            return redirect('create_referral')  # Adjust the redirect to match your URL name if needed

        # Create the ReferralSlip
        ReferralSlip.objects.create(
            from_user=request.user,
            to_member=to_member,
            referral_description=referral_description,
            referral_type=referral_type,
            referral_status=referral_status,
            address=address,
            telephone=telephone,
            email=email,
            comments=comments,
            referral_heat=referral_heat
        )
        messages.success(request, "Referral created successfully.")
        return redirect('list_referrals')  # Adjust the redirect to match your URL name if needed
    else:
        # This is where you handle GET requests and any other methods
        members = User.objects.all()
        return render(request, 'referrals/create_referral.html', {'members': members})
    
    
@login_required
def list_referrals(request):
    referrals = ReferralSlip.objects.filter(from_user=request.user)
    return render(request, 'referrals/list_referrals.html', {'referrals': referrals})


@login_required
def referral_report(request):
    if request.method == 'POST':
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')

        if from_date and to_date:
            from_date = parse_date(from_date)
            to_date = parse_date(to_date)
            referrals = ReferralSlip.objects.filter(
                Q(date__gte=from_date) & Q(date__lte=to_date)
            )
        else:
            referrals = ReferralSlip.objects.all()

        return render(request, 'referrals/referral_report.html', {
            'referrals': referrals,
            'from_date': from_date,
            'to_date': to_date
        })
    else:
        return render(request, 'referrals/referral_report.html')