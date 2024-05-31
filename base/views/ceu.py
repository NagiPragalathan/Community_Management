from django.shortcuts import render, get_object_or_404, redirect
from .models import ChapterEdUnit
from .forms import ChapterEdUnitForm, QtyEarnedForm

def chapteredunit_list(request):
    chapteredunits = ChapterEdUnit.objects.all()
    return render(request, 'ceu/chapteredunit_list.html', {'chapteredunits': chapteredunits})

def chapteredunit_detail(request, pk):
    chapteredunit = get_object_or_404(ChapterEdUnit, pk=pk)
    return render(request, 'ceu/chapteredunit_detail.html', {'chapteredunit': chapteredunit})

def chapteredunit_create(request):
    if request.method == "POST":
        form = ChapterEdUnitForm(request.POST)
        if form.is_valid():
            chapteredunit = form.save()
            return redirect('chapteredunit_detail', pk=chapteredunit.pk)
    else:
        form = ChapterEdUnitForm()
    return render(request, 'ceu/chapteredunit_form.html', {'form': form})

def qty_earned_edit(request, pk):
    chapteredunit = get_object_or_404(ChapterEdUnit, pk=pk)
    if request.method == "POST":
        form = QtyEarnedForm(request.POST, instance=chapteredunit)
        if form.is_valid():
            chapteredunit = form.save()
            return redirect('chapteredunit_detail', pk=chapteredunit.pk)
    else:
        form = QtyEarnedForm(instance=chapteredunit)
    return render(request, 'ceu/qty_earned_form.html', {'form': form})
