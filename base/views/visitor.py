from django.shortcuts import render, redirect
from base.models import Visitor


def register_visitor(request):
    if request.method == 'POST':
        visitor = Visitor(
            title=request.POST.get('title', ''),
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            suffix=request.POST.get('suffix', ''),
            email=request.POST['email'],
            phone_number=request.POST['phone_number'],
            company_name=request.POST.get('company_name', ''),
            address_line_1=request.POST.get('address_line_1', ''),
            address_line_2=request.POST.get('address_line_2', ''),
            city=request.POST.get('city', ''),
            state=request.POST.get('state', ''),
            post_code=request.POST.get('post_code', ''),
            category=request.POST['category'],
            visitor_type=request.POST['visitor_type'],
            visit_date=request.POST['visit_date']
        )
        visitor.save()
        return redirect('success_page')  # Redirect to a new URL if the form is successfully submitted
    return render(request, 'register_visitor.html')


def visitor_registration(request):
    chapters = Chapter.objects.all()  # Assuming you have a Chapter model
    categories = Category.objects.all()  # Assuming you have a Category model
    context = {
        'chapters': chapters,
        'categories': categories,
    }
    return render(request, 'visitor_registration.html', context)