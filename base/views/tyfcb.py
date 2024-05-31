from django.shortcuts import render, get_object_or_404, redirect
from base.models import TYFCB
from base.forms import TYFCBForm

def tyfcb_list(request):
    tyfcbs = TYFCB.objects.all()
    return render(request, 'tyfcb/tyfcb_list.html', {'tyfcbs': tyfcbs})

def tyfcb_detail(request, pk):
    tyfcb = get_object_or_404(TYFCB, pk=pk)
    return render(request, 'tyfcb/tyfcb_detail.html', {'tyfcb': tyfcb})

def tyfcb_create(request):
    if request.method == "POST":
        form = TYFCBForm(request.POST)
        if form.is_valid():
            tyfcb = form.save()
            return redirect('tyfcb_detail', pk=tyfcb.pk)
    else:
        form = TYFCBForm()
    return render(request, 'tyfcb/tyfcb_form.html', {'form': form})

def tyfcb_edit(request, pk):
    tyfcb = get_object_or_404(TYFCB, pk=pk)
    if request.method == "POST":
        form = TYFCBForm(request.POST, instance=tyfcb)
        if form.is_valid():
            tyfcb = form.save()
            return redirect('tyfcb_detail', pk=tyfcb.pk)
    else:
        form = TYFCBForm(instance=tyfcb)
    return render(request, 'tyfcb/tyfcb_form.html', {'form': form})
