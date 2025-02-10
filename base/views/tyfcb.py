from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from base.models import TYFCB, ChapterName, Region
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from base.forms import TYFCBForm
from django.db.models import Q
from django.core.paginator import Paginator


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
        try:
            # Print debug information
            print(f"Debug - POST data: {request.POST}")
            
            # Validate required fields
            required_fields = ['chapter_name', 'region_name', 'referral_amount', 
                             'business_type', 'referral_type', 'start_date', 'end_date']
            
            for field in required_fields:
                if not request.POST.get(field):
                    raise ValueError(f"{field.replace('_', ' ').title()} is required")

            tyfcb = TYFCB.objects.create(
                user=request.user,
                chapter_name_id=request.POST.get('chapter_name'),
                region_name_id=request.POST.get('region_name'),
                referral_amount=request.POST.get('referral_amount'),
                business_type=request.POST.get('business_type'),
                referral_type=request.POST.get('referral_type'),  # Make sure this is being submitted
                thank_you_to_id=request.POST.get('thank_you_to') if request.POST.get('thank_you_to') else None,
                comments=request.POST.get('comments', ''),
                start_date=request.POST.get('start_date'),
                end_date=request.POST.get('end_date')
            )
            messages.success(request, 'TYFCB created successfully!')
            return redirect('tyfcb_detail', pk=tyfcb.pk)
        except Exception as e:
            messages.error(request, f'Error creating TYFCB: {str(e)}')
            
    # Get choices for the template
    referral_type_choices = TYFCB.REFERRAL_TYPE_CHOICES
    business_type_choices = TYFCB.BUSINESS_TYPE_CHOICES
    
    context = {
        'chapters': ChapterName.objects.all(),
        'regions': Region.objects.all(),
        'users': User.objects.exclude(id=request.user.id).order_by('username'),
        'referral_type_choices': referral_type_choices,
        'business_type_choices': business_type_choices,
    }
    return render(request, 'tyfcb/tyfcb_form.html', context)

@login_required
def tyfcb_edit(request, pk):
    tyfcb = get_object_or_404(TYFCB, pk=pk, user=request.user)

    if request.method == "POST":
        try:
            chapter = ChapterName.objects.get(id=request.POST.get('chapter_name'))
            region = Region.objects.get(id=request.POST.get('region_name'))
            thank_you_to = User.objects.get(id=request.POST.get('thank_you_to')) if request.POST.get('thank_you_to') else None

            tyfcb.chapter_name = chapter
            tyfcb.region_name = region
            tyfcb.referral_amount = request.POST.get('referral_amount')
            tyfcb.business_type = request.POST.get('business_type')
            tyfcb.referral_type = request.POST.get('referral_type')
            tyfcb.thank_you_to = thank_you_to
            tyfcb.comments = request.POST.get('comments')
            tyfcb.start_date = request.POST.get('start_date')
            tyfcb.end_date = request.POST.get('end_date')
            tyfcb.save()
            
            messages.success(request, 'TYFCB updated successfully!')
            return redirect('tyfcb_detail', pk=tyfcb.pk)
        except Exception as e:
            messages.error(request, f'Error updating TYFCB: {str(e)}')

    context = {
        'tyfcb': tyfcb,
        'chapters': ChapterName.objects.all(),
        'regions': Region.objects.all(),
        'users': User.objects.exclude(id=request.user.id).order_by('username')
    }
    return render(request, 'tyfcb/tyfcb_form.html', context)

@login_required
def tyfcb_delete(request, pk):
    tyfcb = get_object_or_404(TYFCB, pk=pk, user=request.user)
    if request.method == "POST":
        tyfcb.delete()
        messages.success(request, 'TYFCB deleted successfully!')
        return redirect('tyfcb_list')
    return render(request, 'tyfcb/tyfcb_confirm_delete.html', {'tyfcb': tyfcb})

@login_required
def tyfcb_list(request):
    # Get filter parameters
    form = request.GET
    start_date = form.get('start_date')
    end_date = form.get('end_date')
    chapter_id = form.get('chapter')
    search_query = form.get('search')
    
    # Base query
    query = Q(user=request.user)
    
    # Apply filters
    if start_date and end_date:
        query &= Q(start_date__range=[start_date, end_date])
    if chapter_id:
        query &= Q(chapter_name_id=chapter_id)
    if search_query:
        query &= (Q(comments__icontains=search_query) | 
                 Q(thank_you_to__username__icontains=search_query))

    # Get queryset with filters
    tyfcbs = TYFCB.objects.filter(query).select_related(
        'chapter_name', 'region_name', 'thank_you_to'
    ).order_by('-start_date')
    
    # Pagination
    paginator = Paginator(tyfcbs, 10)
    page = request.GET.get('page')
    tyfcbs = paginator.get_page(page)
    
    context = {
        'tyfcbs': tyfcbs,
        'chapters': ChapterName.objects.all(),
        'regions': Region.objects.all(),
        'start_date': start_date,
        'end_date': end_date,
        'selected_chapter': chapter_id,
        'search_query': search_query
    }
    return render(request, 'tyfcb/tyfcb_list.html', context)

