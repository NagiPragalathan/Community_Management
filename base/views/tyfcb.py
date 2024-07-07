from django.shortcuts import render, get_object_or_404, redirect
from base.models import TYFCB
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from base.forms import TYFCBForm
from django.db.models import Q  # Import the Q object here


# @login_required
# def tyfcb_list(request):
#     # Only show TYFCBs related to the logged-in user
#     tyfcbs = TYFCB.objects.filter(user=request.user)
#     return render(request, 'tyfcb/tyfcb_list.html', {'tyfcbs': tyfcbs})

@login_required
def tyfcb_detail(request, pk):
    tyfcb = get_object_or_404(TYFCB, pk=pk, user=request.user)
    return render(request, 'tyfcb/tyfcb_detail.html', {'tyfcb': tyfcb})

@login_required
def tyfcb_create(request):
    if request.method == "POST":
        chapter_name = request.POST.get('chapter_name')
        region_name = request.POST.get('region_name')
        referral_amount = request.POST.get('referral_amount')
        business_type = request.POST.get('business_type')
        referral_type = request.POST.get('referral_type')
        thank_you_to_id = request.POST.get('thank_you_to')
        comments = request.POST.get('comments')

        thank_you_to = User.objects.get(id=thank_you_to_id) if thank_you_to_id else None

        tyfcb = TYFCB.objects.create(
            user=request.user,
            chapter_name=chapter_name,
            region_name=region_name,
            referral_amount=referral_amount,
            business_type=business_type,
            referral_type=referral_type,
            thank_you_to=thank_you_to,
            comments=comments
        )
        return redirect('tyfcb_detail', pk=tyfcb.pk)
    
    users = User.objects.all()
    return render(request, 'tyfcb/tyfcb_form.html', {'users': users})

@login_required
def tyfcb_edit(request, pk):
    tyfcb = get_object_or_404(TYFCB, pk=pk, user=request.user)  # Ensure user is editing their own record

    if request.method == "POST":
        chapter_name = request.POST.get('chapter_name')
        region_name = request.POST.get('region_name')
        referral_amount = request.POST.get('referral_amount')
        business_type = request.POST.get('business_type')
        referral_type = request.POST.get('referral_type')
        thank_you_to_id = request.POST.get('thank_you_to')
        comments = request.POST.get('comments')

        thank_you_to = User.objects.get(id=thank_you_to_id) if thank_you_to_id else None

        tyfcb.chapter_name = chapter_name
        tyfcb.region_name = region_name
        tyfcb.referral_amount = referral_amount
        tyfcb.business_type = business_type
        tyfcb.referral_type = referral_type
        tyfcb.thank_you_to = thank_you_to
        tyfcb.comments = comments
        tyfcb.save()

        return redirect('tyfcb_detail', pk=tyfcb.pk)
    
    users = User.objects.all()
    return render(request, 'tyfcb/tyfcb_form.html', {'tyfcb': tyfcb, 'users': users})


@login_required
def tyfcb_list(request):
    form = request.GET
    start_date = form.get('start_date')
    end_date = form.get('end_date')
    query = Q(user=request.user)  # Filter by logged-in user

    if start_date and end_date:
        query &= Q(start_date__gte=start_date) & Q(end_date__lte=end_date)
    
    tyfcbs = TYFCB.objects.filter(query)
    return render(request, 'tyfcb/tyfcb_review.html', {'tyfcbs': tyfcbs, 'start_date': start_date, 'end_date': end_date})

