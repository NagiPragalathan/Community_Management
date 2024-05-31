from django.shortcuts import render, get_object_or_404, redirect
from base.models import OneToOneSlip
from base.forms import OneToOneSlipForm

def one_to_one_slip_list(request):
    one_to_one_slips = OneToOneSlip.objects.all()
    return render(request, 'oneslip/list.html', {'one_to_one_slips': one_to_one_slips})

def one_to_one_slip_detail(request, pk):
    one_to_one_slip = get_object_or_404(OneToOneSlip, pk=pk)
    return render(request, 'oneslip/detail.html', {'one_to_one_slip': one_to_one_slip})

def one_to_one_slip_create(request):
    if request.method == "POST":
        form = OneToOneSlipForm(request.POST)
        if form.is_valid():
            one_to_one_slip = form.save()
            return redirect('one_to_one_slip_detail', pk=one_to_one_slip.pk)
    else:
        form = OneToOneSlipForm()
    return render(request, 'oneslip/form.html', {'form': form})

def one_to_one_slip_edit(request, pk):
    one_to_one_slip = get_object_or_404(OneToOneSlip, pk=pk)
    if request.method == "POST":
        form = OneToOneSlipForm(request.POST, instance=one_to_one_slip)
        if form.is_valid():
            one_to_one_slip = form.save()
            return redirect('one_to_one_slip_detail', pk=one_to_one_slip.pk)
    else:
        form = OneToOneSlipForm(instance=one_to_one_slip)
    return render(request, 'oneslip/form.html', {'form': form})
