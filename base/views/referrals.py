from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from base.models import ReferralSlip, Member
from django.urls import path


@login_required
def create_referral(request):
    if request.method == 'POST':
        # Extract form data
        to_member_id = request.POST.get('to_member')
        referral_description = request.POST.get('referral')
        referral_type = request.POST.get('referral_type')
        referral_status = request.POST.get('referral_status')
        address = request.POST.get('address', '')
        telephone = request.POST.get('telephone')
        email = request.POST.get('email', '')
        comments = request.POST.get('comments', '')
        referral_heat = request.POST.get('referral_heat')

        # Create referral slip
        ReferralSlip.objects.create(
            from_user=request.user,
            to_member_id=to_member_id,
            referral_description=referral_description,
            referral_type=referral_type,
            referral_status=referral_status,
            address=address,
            telephone=telephone,
            email=email,
            comments=comments,
            referral_heat=referral_heat
        )
        return redirect('referrals/list_referrals')

    # If GET request or other, just show the form
    members = Member.objects.all()  # Assuming Member model stores chapter members
    return render(request, 'referrals/create_referral.html', {'members': members})

@login_required
def list_referrals(request):
    referrals = ReferralSlip.objects.filter(from_user=request.user)
    return render(request, 'referrals/list_referrals.html', {'referrals': referrals})
