from django.shortcuts import render, get_object_or_404, redirect
from base.models import TYFCB
from django.contrib.auth.decorators import login_required
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
        form = TYFCBForm(request.POST)
        if form.is_valid():
            tyfcb = form.save(commit=False)
            tyfcb.user = request.user  # Set the user to the currently logged-in user
            tyfcb.save()
            return redirect('tyfcb_detail', pk=tyfcb.pk)
    else:
        form = TYFCBForm()
    return render(request, 'tyfcb/tyfcb_form.html', {'form': form})

@login_required
def tyfcb_edit(request, pk):
    tyfcb = get_object_or_404(TYFCB, pk=pk, user=request.user)  # Ensure user is editing their own record
    if request.method == "POST":
        form = TYFCBForm(request.POST, instance=tyfcb)
        if form.is_valid():
            tyfcb = form.save()
            return redirect('tyfcb_detail', pk=tyfcb.pk)
    else:
        form = TYFCBForm(instance=tyfcb)
    return render(request, 'tyfcb/tyfcb_form.html', {'form': form})

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