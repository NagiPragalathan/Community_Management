from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from base.models import Referral
from base.forms import ReferralForm

def referral_list(request):
    referrals = Referral.objects.all()
    return render(request, 'referrals/referral_list.html', {'referrals': referrals})

def referral_detail(request, pk):
    referral = get_object_or_404(Referral, pk=pk)
    return render(request, 'referrals/referral_detail.html', {'referral': referral})

@login_required
def referral_create(request):
    if request.method == "POST":
        form = ReferralForm(request.POST)
        if form.is_valid():
            referral = form.save(commit=False)
            referral.user = request.user  # Assign the current user as the referrer
            referral.save()
            return redirect('referral_detail', pk=referral.pk)
    else:
        form = ReferralForm()
    return render(request, 'referrals/referral_form.html', {'form': form})

@login_required
def referral_edit(request, pk):
    referral = get_object_or_404(Referral, pk=pk)
    if request.method == "POST":
        form = ReferralForm(request.POST, instance=referral)
        if form.is_valid():
            referral = form.save(commit=False)
            referral.user = request.user  # Re-assign the user in case it’s necessary
            referral.save()
            return redirect('referral_detail', pk=referral.pk)
    else:
        form = ReferralForm(instance=referral)
    return render(request, 'referrals/referral_form.html', {'form': form})
