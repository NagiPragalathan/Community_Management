from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from base.models import Industry, Classification

# Industry CRUD operations
@login_required
def industry_list(request):
    industries = Industry.objects.all().order_by('name')
    return render(request, 'base_profile/industry_list.html', {'industries': industries})

@login_required
def industry_detail(request, pk):
    industry = get_object_or_404(Industry, pk=pk)
    return render(request, 'base_profile/industry_detail.html', {'industry': industry})

@login_required
def industry_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        Industry.objects.create(name=name, description=description)
        return redirect('industry_list')
    return render(request, 'base_profile/industry_form.html')

@login_required
def industry_update(request, pk):
    industry = get_object_or_404(Industry, pk=pk)
    if request.method == 'POST':
        industry.name = request.POST.get('name')
        industry.description = request.POST.get('description')
        industry.save()
        return redirect('industry_list')
    return render(request, 'base_profile/industry_form.html', {'industry': industry})

@login_required
def industry_delete(request, pk):
    industry = get_object_or_404(Industry, pk=pk)
    if request.method == 'POST':
        industry.delete()
        return redirect('industry_list')
    return render(request, 'base_profile/industry_confirm_delete.html', {'industry': industry})

# Classification CRUD operations
@login_required
def classification_list(request):
    classifications = Classification.objects.all().order_by('name')
    return render(request, 'base_profile/classification_list.html', {'classifications': classifications})

@login_required
def classification_detail(request, pk):
    classification = get_object_or_404(Classification, pk=pk)
    return render(request, 'base_profile/classification_detail.html', {'classification': classification})

@login_required
def classification_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        Classification.objects.create(name=name, description=description)
        return redirect('classification_list')
    return render(request, 'base_profile/classification_form.html')

@login_required
def classification_update(request, pk):
    classification = get_object_or_404(Classification, pk=pk)
    if request.method == 'POST':
        classification.name = request.POST.get('name')
        classification.description = request.POST.get('description')
        classification.save()
        return redirect('classification_list')
    return render(request, 'base_profile/classification_form.html', {'classification': classification})

@login_required
def classification_delete(request, pk):
    classification = get_object_or_404(Classification, pk=pk)
    if request.method == 'POST':
        classification.delete()
        return redirect('classification_list')
    return render(request, 'base_profile/classification_confirm_delete.html', {'classification': classification}) 